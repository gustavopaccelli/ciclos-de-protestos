"""extrai_camara_senado.py — Atos legislativos federais por janela de ciclo.

Consulta a API de Dados Abertos da Câmara dos Deputados (v2) e emite linhas já
no schema de process-tracing/dados/registro_evidencias.csv, com
status_verificacao=verificado_fonte_oficial e a URL da própria API como fonte.

ATENÇÃO — NÃO TESTADO CONTRA A API. O ambiente onde este script foi escrito
bloqueia todo egresso de rede (403 no CONNECT para dadosabertos.camara.leg.br).
A estrutura das requisições segue a documentação pública da API v2, mas a
primeira execução com rede deve começar por --dry-run e conferir o retorno.

COBERTURA HISTÓRICA — LIMITE IMPORTANTE
A API cobre bem o período recente. Para 1983-1992 (C1 e C2) o acervo digital é
irregular: proposições antigas existem, mas votações nominais frequentemente
não. Para esses ciclos a fonte primária é o Diário da Câmara/Congresso
digitalizado em imagem.camara.gov.br, que não tem API — a recuperação é manual,
pelo caminho documentado em fontes/registro-fontes.md.

Uso:
  python extrai_camara_senado.py --ciclo c2 --dry-run
  python extrai_camara_senado.py --ciclo c4 --tipo PEC --saida novas_evidencias.csv
"""

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
API = "https://dadosabertos.camara.leg.br/api/v2"
PAUSA = 0.5          # cortesia com o servidor público
TIMEOUT = 30

# Janelas por ciclo: (inicio_T-1c, fim_T+1). Derivadas de data/cycle_phases.csv
# com a janela_fixa de 24 meses do codebook. Para C1 o T+1 é estendido até 1989
# porque a cadeia C1->C2 (Constituinte, CF/88, eleição direta) é o T-1 de C2.
JANELAS = {
    "c1": ("1980-11-15", "1989-12-31"),
    "c2": ("1989-11-01", "1994-12-31"),
    "c3": ("2011-06-06", "2015-12-31"),
    "c4": ("2012-10-27", "2018-09-30"),
}


def get(caminho: str, **params) -> dict:
    """GET na API com paginação transparente e erro legível."""
    url = f"{API}/{caminho}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"[HTTP {e.code}] {url}\n{e.read()[:400].decode('utf-8', 'replace')}")
    except urllib.error.URLError as e:
        raise SystemExit(
            f"[rede] {url}\n{e.reason}\n"
            "Se o erro for 403 no CONNECT, a rede está bloqueada por proxy — "
            "rode este script em máquina com acesso à internet."
        )


def paginar(caminho: str, limite: int | None = None, **params):
    """Itera todas as páginas de um endpoint de lista."""
    params.setdefault("itens", 100)
    pagina, vistos = 1, 0
    while True:
        dados = get(caminho, pagina=pagina, **params)
        itens = dados.get("dados", [])
        if not itens:
            return
        for item in itens:
            yield item
            vistos += 1
            if limite and vistos >= limite:
                return
        if not any(l.get("rel") == "next" for l in dados.get("links", [])):
            return
        pagina += 1
        time.sleep(PAUSA)


def busca_proposicoes(ciclo: str, tipos: list[str], limite: int | None):
    inicio, fim = JANELAS[ciclo]
    for tipo in tipos:
        print(f"  [{ciclo}] {tipo} de {inicio} a {fim}", file=sys.stderr)
        yield from paginar(
            "proposicoes",
            limite=limite,
            siglaTipo=tipo,
            dataApresentacaoInicio=inicio,
            dataApresentacaoFim=fim,
            ordem="ASC",
            ordenarPor="id",
        )


def para_linha_de_evidencia(prop: dict, ciclo: str, seq: int) -> dict:
    """Converte a proposição no schema do registro. Campos analíticos ficam
    vazios de propósito: mecanismo, teste_van_evera e hipotese_vinculada são
    julgamento do pesquisador, não da API."""
    pid = prop.get("id")
    return {
        "evidencia_id": f"EV-{ciclo.upper()}-API-{seq:04d}",
        "ciclo": ciclo,
        "tempo": "",
        "data_evento": prop.get("dataApresentacao", "")[:10],
        "fase_vinculada": "",
        "dimensao_conjuntura": "acontecimentos",
        "mecanismo": "",
        "descricao": f"{prop.get('siglaTipo')} {prop.get('numero')}/{prop.get('ano')} — "
                     f"{(prop.get('ementa') or '').strip()}",
        "hipotese_vinculada": "",
        "relacao_com_hipotese": "",
        "teste_van_evera": "",
        "fonte_nivel": 1,
        "fonte_citacao": f"Câmara dos Deputados, API de Dados Abertos v2, proposição {pid}",
        "fonte_url": f"{API}/proposicoes/{pid}",
        "data_consulta": date.today().isoformat(),
        "status_verificacao": "verificado_fonte_oficial",
        "divergencia_entre_fontes": "",
        "notas": "Importado automaticamente. Classificar tempo, mecanismo, hipótese e "
                 "teste diagnóstico manualmente antes de usar na análise.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ciclo", required=True, choices=sorted(JANELAS))
    ap.add_argument("--tipo", action="append", default=None,
                    help="sigla do tipo (PEC, PL, PLP, MPV...). Repetível. Padrão: PEC e PDC")
    ap.add_argument("--limite", type=int, default=None, help="máximo de itens (teste)")
    ap.add_argument("--saida", default=None, help="CSV de saída; padrão: stdout resumido")
    ap.add_argument("--dry-run", action="store_true",
                    help="lista o que seria coletado, sem gravar")
    args = ap.parse_args()

    tipos = args.tipo or ["PEC", "PDC"]
    linhas = [para_linha_de_evidencia(p, args.ciclo, i)
              for i, p in enumerate(busca_proposicoes(args.ciclo, tipos, args.limite), 1)]

    print(f"\n{len(linhas)} proposições na janela de {args.ciclo}")
    for l in linhas[:10]:
        print(f"  {l['data_evento']}  {l['descricao'][:100]}")
    if len(linhas) > 10:
        print(f"  ... e mais {len(linhas) - 10}")

    if args.dry_run:
        print("\n--dry-run: nada gravado.")
        return
    if not args.saida:
        print("\nSem --saida: nada gravado. Informe o arquivo para persistir.")
        return

    destino = Path(args.saida)
    with destino.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"\n{len(linhas)} linhas → {destino}")
    print("Revise e só então concatene em dados/registro_evidencias.csv.")


if __name__ == "__main__":
    main()
