"""executa_coleta.py — Orquestra a coleta completa em máquina com rede.

Roda os dois extratores para todos os ciclos e grava dados/relatorio_coleta.md
com o que foi recuperado, o que falhou e o que continua pendente.

Testa a conectividade ANTES de tentar coletar: sem rede, os extratores falhariam
host a host com mensagens confusas. Aqui o diagnóstico vem primeiro e diz onde
rodar.

Uso:
  python executa_coleta.py --dry-run     # só diagnostica a rede
  python executa_coleta.py               # coleta completa
  python executa_coleta.py --ciclo c2    # um ciclo só
"""

import argparse
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCRIPTS = BASE / "scripts"
RELATORIO = BASE / "dados" / "relatorio_coleta.md"
CICLOS = ["c1", "c2", "c3", "c4"]

HOSTS = {
    "dadosabertos.camara.leg.br": "proposições, tramitação e votações da Câmara",
    "legis.senado.leg.br": "matérias e votações do Senado",
    "api.bcb.gov.br": "séries macroeconômicas (BCB-SGS)",
    "servicodados.ibge.gov.br": "agregados do IBGE/SIDRA",
    "dadosabertos.tse.jus.br": "resultados eleitorais",
    "imagem.camara.gov.br": "Diários digitalizados (recuperação manual)",
}


def testa(host: str, timeout: int = 12) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(f"https://{host}/", method="HEAD",
                                     headers={"User-Agent": "PesquisaAcademicaAEP/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return True, f"HTTP {e.code} (host alcançável)"
    except (urllib.error.URLError, ssl.SSLError, socket.timeout, OSError) as e:
        return False, str(getattr(e, "reason", e))[:80]


def diagnostica() -> dict[str, tuple[bool, str]]:
    print("Testando conectividade com as fontes oficiais...\n")
    res = {}
    for host, desc in HOSTS.items():
        ok, msg = testa(host)
        res[host] = (ok, msg)
        print(f"  {'OK  ' if ok else 'FALHA'}  {host:<32} {msg}")
        if not ok:
            print(f"          ({desc})")
    return res


def roda(script: str, *args: str) -> tuple[bool, str]:
    cmd = [sys.executable, str(SCRIPTS / script), *args]
    print(f"\n$ {' '.join(cmd[1:])}")
    p = subprocess.run(cmd, capture_output=True, text=True)
    saida = (p.stdout or "") + (p.stderr or "")
    print(saida.rstrip()[:2000])
    return p.returncode == 0, saida


def escreve_relatorio(diag, execucoes, ciclos) -> None:
    alcancaveis = sum(1 for ok, _ in diag.values() if ok)
    L = [f"# Relatório de coleta — {date.today().isoformat()}", "",
         f"Hosts alcançáveis: {alcancaveis} de {len(diag)}.", "",
         "## Conectividade", "", "| Host | Estado | Detalhe |", "|---|---|---|"]
    for host, (ok, msg) in diag.items():
        L.append(f"| `{host}` | {'alcançável' if ok else 'BLOQUEADO'} | {msg} |")
    L += ["", "## Execuções", ""]
    if not execucoes:
        L.append("Nenhuma execução: rede indisponível.")
    for nome, ok, saida in execucoes:
        L += [f"### {nome}", "", f"Estado: {'sucesso' if ok else 'FALHA'}", "",
              "```", saida.rstrip()[:3000], "```", ""]
    L += ["## Pendências que nenhum script resolve", "",
          "Os Diários da Câmara e do Congresso digitalizados são imagem, sem API e sem",
          "indexação de texto. As páginas exatas estão em `fontes/fontes-de-dados.csv`:", "",
          "- Diário da Câmara, 30/09/1992, p. 22067 — placar do impeachment de Collor",
          "- Diário do Congresso, 30/12/1992, p. 4811 — abertura do julgamento no Senado",
          "- Diário do Senado, 31/08/2016 — ata do julgamento de Dilma", "",
          "Abra-as manualmente e atualize `status_verificacao` e `fonte_nivel` no registro.", "",
          "## Depois da coleta", "",
          "```bash",
          "python process-tracing/scripts/valida_registro.py --estrito",
          "python process-tracing/scripts/gera_planilha_fontes.py",
          "```"]
    RELATORIO.write_text("\n".join(L), encoding="utf-8")
    print(f"\nRelatório → {RELATORIO}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ciclo", choices=CICLOS, default=None)
    ap.add_argument("--dry-run", action="store_true", help="só diagnostica a rede")
    args = ap.parse_args()

    diag = diagnostica()
    bloqueados = [h for h, (ok, _) in diag.items() if not ok]

    if bloqueados:
        print(f"\n{len(bloqueados)} de {len(diag)} hosts inalcançáveis.")
        if len(bloqueados) == len(diag):
            print("\nTodos bloqueados — este ambiente não tem egresso para as fontes oficiais.")
            print("Rode este script em máquina com acesso à internet aberta.")
            escreve_relatorio(diag, [], CICLOS)
            return
        print("Coleta parcial: os extratores dos hosts bloqueados vão falhar.")

    if args.dry_run:
        print("\n--dry-run: nada coletado.")
        escreve_relatorio(diag, [], CICLOS)
        return

    ciclos = [args.ciclo] if args.ciclo else CICLOS
    execucoes = []
    for c in ciclos:
        ok, saida = roda("extrai_camara_senado.py", "--ciclo", c,
                         "--saida", str(BASE / "dados" / f"candidatos_{c}.csv"))
        execucoes.append((f"extrai_camara_senado.py --ciclo {c}", ok, saida))
    ok, saida = roda("extrai_series_estruturais.py", "--indicador", "inflacao")
    execucoes.append(("extrai_series_estruturais.py --indicador inflacao", ok, saida))

    escreve_relatorio(diag, execucoes, ciclos)
    print("\nOs CSVs de candidatos exigem classificação manual (tempo, mecanismo,")
    print("hipótese, teste diagnóstico) antes de entrar no registro. Ver PROTOCOLO §8.")


if __name__ == "__main__":
    main()
