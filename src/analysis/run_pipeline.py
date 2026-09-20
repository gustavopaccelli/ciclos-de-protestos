"""Orquestrador da pipeline PEA.

Uso:
  python run_pipeline.py --step scrape            # coleta (horas-dias; retomável)
  python run_pipeline.py --step code --batch 100  # codificação em lotes
  python run_pipeline.py --step build             # dataset final CSV/XLSX
  python run_pipeline.py --step kappa --manual amostra.csv   # confiabilidade
  python run_pipeline.py --step all

`all` roda scrape → code → build. A aferição de kappa (Passagem 5 do
protocolo) exige uma amostra codificada à mão e por isso é sempre explícita.
"""

import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
STEPS = {
    "scrape": ["01_scraper.py"],
    "code": ["02_doca_coder.py"],
    "build": ["03_build_dataset.py"],
    "kappa": ["04_intercoder_reliability.py"],
}

# Passos executados por `--step all`. `kappa` fica de fora porque depende de
# uma amostra codificada manualmente, passada em --manual.
ALL_STEPS = ["scrape", "code", "build"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=[*STEPS, "all"], required=True)
    ap.add_argument("--batch", type=int, default=None)
    ap.add_argument("--manual", default=None,
                    help="CSV da codificação manual (obrigatório em --step kappa)")
    args = ap.parse_args()

    if args.step == "kappa" and not args.manual:
        raise SystemExit("--step kappa exige --manual <amostra.csv>")

    order = ALL_STEPS if args.step == "all" else [args.step]
    for step in order:
        cmd = [sys.executable, str(BASE / STEPS[step][0])]
        if step == "code" and args.batch:
            cmd += ["--batch", str(args.batch)]
        if step == "kappa":
            cmd += [args.manual]
        print(f"\n=== {step} ===")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
