#!/usr/bin/env python3
"""Atribui ciclo e fase a eventos pela data, a partir do cycle_phases.csv.

Regra do codebook AEP-BR v1.0: a variável `ciclo` não é codificada à mão; é
derivada da data de início do evento. Datas fora de todas as janelas recebem
`fora_de_ciclo`.

Uso:
    python src/analysis/atribui_ciclo.py 1984-04-16 2013-06-17
    python src/analysis/atribui_ciclo.py --csv eventos.csv --coluna data_inicio --saida saida.csv
"""
import argparse
import csv
import sys
from datetime import date
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

CYCLE_PHASES = paths.PROCESSED / "cycle_phases" / "cycle_phases.csv"
FORA = "fora_de_ciclo"


@lru_cache(maxsize=1)
def _fases():
    with open(CYCLE_PHASES, encoding="utf-8") as f:
        return [
            (date.fromisoformat(r["date_start"]), date.fromisoformat(r["date_end"]),
             r["cycle"], r["phase_id"])
            for r in csv.DictReader(f)
        ]


def ciclo_e_fase(data):
    """Devolve (ciclo, phase_id) para uma data ISO; (fora_de_ciclo, None) se não houver."""
    d = date.fromisoformat(str(data)[:10])
    for ini, fim, ciclo, fase in _fases():
        if ini <= d <= fim:
            return ciclo, fase
    return FORA, None


def ciclo_para_data(data):
    return ciclo_e_fase(data)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datas", nargs="*")
    ap.add_argument("--csv")
    ap.add_argument("--coluna", default="data_inicio")
    ap.add_argument("--saida")
    a = ap.parse_args()

    for d in a.datas:
        print(d, *ciclo_e_fase(d))
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f)
            linhas, campos = list(leitor), leitor.fieldnames
        for r in linhas:
            r["ciclo"], r["fase"] = ciclo_e_fase(r[a.coluna]) if r.get(a.coluna) else (FORA, None)
        novos = [c for c in ("ciclo", "fase") if c not in campos]
        destino = open(a.saida, "w", encoding="utf-8", newline="") if a.saida else sys.stdout
        w = csv.DictWriter(destino, fieldnames=campos + novos)
        w.writeheader()
        w.writerows(linhas)


if __name__ == "__main__":
    main()
