"""Orquestrador da pipeline PEA.

Uso:
  python run_pipeline.py --step scrape            # coleta (horas-dias; retomável)
  python run_pipeline.py --step code --batch 100  # codificação em lotes
  python run_pipeline.py --step build             # dataset final CSV/XLSX
  python run_pipeline.py --step all
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
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=[*STEPS, "all"], required=True)
    ap.add_argument("--batch", type=int, default=None)
    args = ap.parse_args()

    order = list(STEPS) if args.step == "all" else [args.step]
    for step in order:
        cmd = [sys.executable, str(BASE / STEPS[step][0])]
        if step == "code" and args.batch:
            cmd += ["--batch", str(args.batch)]
        print(f"\n=== {step} ===")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
