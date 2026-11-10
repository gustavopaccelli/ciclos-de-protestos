#!/usr/bin/env python3
"""piloto.py — Amostra e planilha cega do piloto de 2013 (tarefas B6 e B11).

  amostra   sorteia N matérias coletadas, estratificadas pela fase do ciclo de
            Junho de 2013 em que a matéria foi publicada (e um estrato para as
            datas fora do ciclo). Alocação igual entre estratos, limitada ao que
            cada um tem; o que sobra vai para os estratos maiores.
  planilha  depois da codificação automática, gera o gold standard para
            codificação manual CEGA: uma linha por evento que o LLM encontrou,
            só com as colunas de identificação preenchidas; as variáveis a
            aferir ficam vazias. Matérias sem evento aparecem numa linha com
            evento_id vazio, para o codificador acrescentar o que o LLM não viu.

Uso (a partir da raiz):
  python src/preprocessing/piloto.py amostra [--n 100] [--janela junho_2013]
  python src/preprocessing/piloto.py planilha
O roteiro completo está em bancos/03_aep_br/validacao/piloto_2013/ROTEIRO.md.
"""
import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from analysis.atribui_ciclo import ciclo_e_fase  # noqa: E402
from build_dataset import parse_data_ptbr  # noqa: E402
from intercoder_reliability import COLUNAS_MANUAIS  # noqa: E402

DIR = paths.AEP_VALIDACAO / "piloto_2013"
AMOSTRA = DIR / "amostra.csv"
GOLD = DIR / "gold_standard.csv"
SEMENTE = 2013
IDENTIFICACAO = ["arquivo", "url", "evento_id", "data_inicio", "cidade"]


def estrato(data_hint: str | None) -> str:
    d = parse_data_ptbr([data_hint]).iloc[0]
    if d is None or str(d) == "NaT":
        return "sem_data"
    ciclo, fase = ciclo_e_fase(d.date().isoformat())
    return fase if ciclo == "junho_2013" else "fora_do_ciclo"


def aloca(tamanhos: dict[str, int], n: int) -> dict[str, int]:
    """Alocação igual, limitada ao tamanho de cada estrato; a sobra vai aos maiores."""
    cota = {e: 0 for e in tamanhos}
    restante = min(n, sum(tamanhos.values()))
    while restante:
        abertos = [e for e in tamanhos if cota[e] < tamanhos[e]]
        for e in sorted(abertos, key=lambda e: -tamanhos[e])[:restante]:
            cota[e] += 1
            restante -= 1
    return cota


def amostra(n: int, janela: str | None, origem: Path = paths.FOLHA_RAW, destino: Path = AMOSTRA) -> None:
    materias = []
    for p in sorted(origem.glob("*.json")):
        art = json.loads(p.read_text(encoding="utf-8"))
        if not art.get("text") or (janela and art.get("date_range") != janela):
            continue
        materias.append({"arquivo": p.name, "url": art.get("url"), "titulo": art.get("title"),
                         "data_publicacao": art.get("date_hint"), "estrato": estrato(art.get("date_hint"))})
    if not materias:
        raise SystemExit(f"Nenhuma matéria com texto em {origem}" + (f" na janela {janela}" if janela else ""))

    por_estrato: dict[str, list] = {}
    for m in materias:
        por_estrato.setdefault(m["estrato"], []).append(m)
    cota = aloca({e: len(v) for e, v in por_estrato.items()}, n)
    rng = random.Random(SEMENTE)
    sorteio = [m for e in sorted(por_estrato) for m in rng.sample(por_estrato[e], cota[e])]

    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sorteio[0]))
        w.writeheader()
        w.writerows(sorteio)
    print(f"{len(sorteio)} matérias sorteadas de {len(materias)} → {destino}")
    for e in sorted(cota):
        print(f"  {e}: {cota[e]} de {len(por_estrato[e])}")


def planilha(amostra_csv: Path = AMOSTRA, codificadas: Path = paths.AEP_CODIFICACAO, destino: Path = GOLD) -> None:
    if destino.exists():
        raise SystemExit(f"{destino} já existe e pode conter codificação manual. "
                         "Renomeie ou apague o arquivo antes de gerar outro.")
    with open(amostra_csv, encoding="utf-8") as f:
        sorteadas = list(csv.DictReader(f))
    linhas, sem_codigo = [], []
    for m in sorteadas:
        p = codificadas / m["arquivo"]
        if not p.exists():
            sem_codigo.append(m["arquivo"])
            continue
        eventos = json.loads(p.read_text(encoding="utf-8")).get("eventos", [])
        base = {"arquivo": m["arquivo"], "url": m["url"]}
        if not eventos:
            linhas.append({**base, "evento_id": "", "data_inicio": "", "cidade": ""})
        for ev in eventos:
            linhas.append({**base, "evento_id": ev["evento_id"],
                           "data_inicio": ev.get("data_inicio") or "", "cidade": ev.get("cidade") or ""})
    if sem_codigo:
        raise SystemExit(f"{len(sem_codigo)} matéria(s) da amostra ainda sem codificação automática "
                         f"(ex.: {sem_codigo[0]}). Rode o coder com --amostra antes.")

    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=IDENTIFICACAO + COLUNAS_MANUAIS)
        w.writeheader()
        w.writerows({**ln, **{c: "" for c in COLUNAS_MANUAIS}} for ln in linhas)
    print(f"{len(linhas)} linhas ({len(sorteadas)} matérias) → {destino}")


def _autoteste() -> None:
    assert aloca({"a": 50, "b": 3, "c": 10}, 30) == {"a": 17, "b": 3, "c": 10}
    assert sum(aloca({"a": 5, "b": 5}, 100).values()) == 10


if __name__ == "__main__":
    _autoteste()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("amostra")
    a.add_argument("--n", type=int, default=100)
    a.add_argument("--janela", default="junho_2013", help="label de date_ranges; '' para todas")
    sub.add_parser("planilha")
    args = ap.parse_args()
    if args.cmd == "amostra":
        amostra(args.n, args.janela or None)
    else:
        planilha()
