"""extrai_series_estruturais.py — Bateria de indicadores do T-1 estrutural.

Preenche process-tracing/dados/series_estruturais.csv com dados oficiais
brasileiros, operacionalizando o Quadro 3 da tese (Chenoweth & Ulfelder, 2015),
que a tese adota como heurística mas nunca mede para o Brasil.

Fontes: BCB-SGS (séries macro) e IBGE/SIDRA (população, urbanização, trabalho).

ATENÇÃO — NÃO TESTADO CONTRA AS APIs. O ambiente onde este script foi escrito
bloqueia todo egresso (403 no CONNECT para api.bcb.gov.br e servicodados.ibge.gov.br).
As requisições seguem a documentação pública. Comece por --listar e --dry-run.

O script NUNCA sobrescreve valor já preenchido a menos que se passe --forcar:
séries oficiais são revisadas retroativamente, e uma revisão silenciosa do IPCA
mudaria a base do argumento sem deixar rastro.

Uso:
  python extrai_series_estruturais.py --listar
  python extrai_series_estruturais.py --indicador inflacao --dry-run
  python extrai_series_estruturais.py --indicador inflacao
"""

import argparse
import csv
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CSV_SERIES = BASE / "dados" / "series_estruturais.csv"
TIMEOUT = 45

# Séries do Sistema Gerenciador de Séries Temporais do Banco Central.
# 433 = IPCA variação mensal (% a.m.) — agregada aqui para o acumulado do ano.
SGS = {
    "inflacao": {
        "codigo": 433,
        "unidade": "% a.a. (acumulado no ano, a partir da variação mensal)",
        "agregacao": "acumulado_composto",
        "orgao": "BCB/IBGE",
        "serie": "SGS 433 — IPCA variação mensal",
    },
}

IBGE_OBS = {
    "urbanizacao": "SIDRA 202 (Censos) / 6579 — requer montagem de série intercensitária",
    "bonus_demografico_jovem": "SIDRA 7358 — projeções por grupo etário",
    "escolaridade": "PNAD/PNADC — mudança metodológica em 2012 quebra a série",
    "crescimento_pib_per_capita": "SIDRA 6784 — Contas Nacionais Trimestrais",
}


def http_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"[HTTP {e.code}] {url}")
    except (urllib.error.URLError, ssl.SSLError) as e:
        raise SystemExit(
            f"[rede] {url}\n{getattr(e, 'reason', e)}\n"
            "403 no CONNECT significa proxy bloqueando — rode em máquina com internet."
        )


def busca_sgs(codigo: int, ano_ini: int, ano_fim: int) -> dict[int, float]:
    """Retorna {ano: variação acumulada no ano} a partir da série mensal."""
    url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
           f"?formato=json&dataInicial=01/01/{ano_ini}&dataFinal=31/12/{ano_fim}")
    mensais = defaultdict(list)
    for reg in http_json(url):
        ano = int(reg["data"].split("/")[-1])
        mensais[ano].append(float(str(reg["valor"]).replace(",", ".")))
    saida = {}
    for ano, vals in mensais.items():
        if len(vals) < 12:
            print(f"  [aviso] {ano}: só {len(vals)} meses — acumulado parcial", file=sys.stderr)
        acum = 1.0
        for v in vals:
            acum *= (1 + v / 100)
        saida[ano] = round((acum - 1) * 100, 4)
    return saida


def carrega_csv() -> list[dict]:
    with CSV_SERIES.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def grava_csv(linhas: list[dict]) -> None:
    with CSV_SERIES.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--indicador")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--forcar", action="store_true",
                    help="sobrescreve valores já preenchidos (revisão de série)")
    ap.add_argument("--listar", action="store_true")
    args = ap.parse_args()

    linhas = carrega_csv()

    if args.listar or not args.indicador:
        nomes = sorted({l["indicador"] for l in linhas})
        print("Indicadores no arquivo:\n")
        for n in nomes:
            preenchidos = sum(1 for l in linhas if l["indicador"] == n and l["valor"])
            total = sum(1 for l in linhas if l["indicador"] == n)
            auto = "automatizável" if n in SGS else "coleta manual"
            obs = IBGE_OBS.get(n, "")
            print(f"  {n:<34} {preenchidos:>3}/{total} preenchidos  [{auto}]")
            if obs:
                print(f"  {'':<34} {obs}")
        if not args.indicador:
            print("\nInforme --indicador para extrair.")
        return

    if args.indicador not in SGS:
        raise SystemExit(
            f"'{args.indicador}' não tem extração automatizada.\n"
            f"Observação: {IBGE_OBS.get(args.indicador, 'sem rota documentada')}\n"
            "Preencha manualmente e registre fonte_url e data_consulta."
        )

    cfg = SGS[args.indicador]
    alvo = [l for l in linhas if l["indicador"] == args.indicador]
    anos = [int(l["ano"]) for l in alvo]
    print(f"Buscando {args.indicador} ({cfg['serie']}) de {min(anos)} a {max(anos)}...")
    valores = busca_sgs(cfg["codigo"], min(anos), max(anos))
    print(f"  {len(valores)} anos retornados")

    hoje = date.today().isoformat()
    url_fonte = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cfg['codigo']}"
                 f"/dados?formato=json")
    alterados = mantidos = 0
    for l in alvo:
        ano = int(l["ano"])
        if ano not in valores:
            continue
        if l["valor"] and not args.forcar:
            mantidos += 1
            continue
        l["valor"] = valores[ano]
        l["unidade"] = cfg["unidade"]
        l["fonte_orgao"] = cfg["orgao"]
        l["fonte_serie"] = cfg["serie"]
        l["fonte_url"] = url_fonte
        l["data_consulta"] = hoje
        l["status_verificacao"] = "verificado_fonte_oficial"
        alterados += 1

    print(f"  {alterados} a gravar | {mantidos} preservados (use --forcar para sobrescrever)")
    if args.dry_run:
        for l in alvo[:8]:
            print(f"    {l['ano']}: {l['valor']}")
        print("  --dry-run: nada gravado.")
        return
    grava_csv(linhas)
    print(f"  gravado em {CSV_SERIES}")


if __name__ == "__main__":
    main()
