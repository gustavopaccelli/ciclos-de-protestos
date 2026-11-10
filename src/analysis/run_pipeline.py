"""Orquestrador da pipeline PEA.

Uso (a partir da raiz):
  python src/analysis/run_pipeline.py --step scrape            # coleta (horas-dias; retomável)
  python src/analysis/run_pipeline.py --step code --batch 100  # codificação em lotes
  python src/analysis/run_pipeline.py --step build             # dataset final CSV/XLSX
  python src/analysis/run_pipeline.py --step kappa --manual bancos/03_aep_br/validacao/amostra_manual.csv
  python src/analysis/run_pipeline.py --step all

`all` roda scrape → code → build. A aferição de kappa (Passagem 5 do
protocolo) exige uma amostra codificada à mão e por isso é sempre explícita.
"""

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

SRC = Path(__file__).resolve().parents[1]
STEPS = {
    "scrape": SRC / "data" / "scraper.py",
    "code": SRC / "preprocessing" / "coder.py",
    "build": SRC / "preprocessing" / "build_dataset.py",
    "kappa": SRC / "preprocessing" / "intercoder_reliability.py",
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
        cmd = [sys.executable, str(STEPS[step])]
        if step == "code" and args.batch:
            cmd += ["--batch", str(args.batch)]
        if step == "kappa":
            out = paths.AEP_VALIDACAO / f"kappa_{date.today().isoformat()}.csv"
            out.parent.mkdir(parents=True, exist_ok=True)
            cmd += [args.manual, "--out", str(out)]
        print(f"\n=== {step} ===")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
