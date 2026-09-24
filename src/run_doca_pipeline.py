#!/usr/bin/env python3
"""DoCA Pipeline Orchestrator: Scraping → Database → Coding."""

import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
STEPS = {
    "init": ["data/init_doca_database.py"],
    "scrape": ["coleta_acervo.py"],
    "load": ["data/load_acervo_to_doca.py"],
    "code": ["analysis/run_pipeline.py"],
}

ALL_STEPS = ["init", "scrape", "load"]

def run_step(step_name: str, step_file: str, extra_args: list = None) -> bool:
    """Execute a pipeline step."""
    cmd = [sys.executable, str(BASE / step_file)]
    if extra_args:
        cmd.extend(extra_args)

    print(f"\n{'='*60}")
    print(f"  STEP: {step_name.upper()}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Step '{step_name}' failed with exit code {e.returncode}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="DoCA Pipeline: scrape Folha archive → code protest events",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_doca_pipeline.py --step all
  python run_doca_pipeline.py --step init
  python run_doca_pipeline.py --step scrape
  python run_doca_pipeline.py --step load
        """,
    )
    parser.add_argument(
        "--step",
        choices=[*STEPS, "all"],
        required=True,
        help="Pipeline step to execute",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=None,
        help="Batch size for coding step (default: process all)",
    )

    args = parser.parse_args()

    # Determine execution order
    if args.step == "all":
        order = ALL_STEPS
    else:
        order = [args.step]

    print("\n" + "="*60)
    print("  DoCA PROTEST EVENTS PIPELINE")
    print("="*60)
    print(f"\nExecuting: {' → '.join(order)}\n")

    # Run steps
    for step in order:
        if step not in STEPS:
            print(f"\n✗ Unknown step: {step}")
            return 1

        step_file = STEPS[step][0]
        extra_args = []

        if not run_step(step, step_file, extra_args):
            print(f"\n✗ Pipeline stopped at step: {step}")
            return 1

    print("\n" + "="*60)
    print("  ✓ PIPELINE COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review preliminary event records in data/protest_events.db")
    print("  2. Run human coding: python run_analysis_pipeline.py --step code")
    print("  3. Build dataset: python run_analysis_pipeline.py --step build")
    print("="*60 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
