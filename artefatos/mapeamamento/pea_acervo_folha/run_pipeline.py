#!/usr/bin/env python3
"""
=============================================================
scripts/run_pipeline.py
Pipeline completo: scraper → coder → dataset

Uso:
  python run_pipeline.py --step all           # pipeline completo
  python run_pipeline.py --step scrape        # só coleta
  python run_pipeline.py --step code --batch 100  # só codifica
  python run_pipeline.py --step build         # só consolida dataset
  python run_pipeline.py --step check         # só confiabilidade
=============================================================
"""

import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def run_step(name: str, batch: int = 50):
    if name in ("all", "scrape"):
        log.info("=" * 60)
        log.info("PASSO 1 — Coleta de artigos (Acervo Folha)")
        log.info("=" * 60)
        from scripts.s01_scraper import run_scraper
        run_scraper()

    if name in ("all", "code"):
        log.info("=" * 60)
        log.info("PASSO 2 — Codificação DoCA via Claude API")
        log.info("=" * 60)
        from scripts.s02_doca_coder import run_coder
        run_coder(batch_size=batch)

    if name in ("all", "build"):
        log.info("=" * 60)
        log.info("PASSO 3 — Consolidação do dataset")
        log.info("=" * 60)
        from scripts.s03_build_dataset import build_dataset
        build_dataset()

    if name in ("all", "check"):
        log.info("=" * 60)
        log.info("PASSO 4 — Confiabilidade intercodificadores")
        log.info("=" * 60)
        from scripts.s04_intercoder_reliability import run_reliability_check
        run_reliability_check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline PEA — Acervo Folha")
    parser.add_argument(
        "--step",
        choices=["all", "scrape", "code", "build", "check"],
        default="all",
        help="Etapa do pipeline a executar (default: all)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=50,
        help="Número de artigos a codificar por execução (default: 50)",
    )
    args = parser.parse_args()

    log.info("Pipeline PEA — Acervo Folha de S.Paulo")
    log.info(f"Executando etapa: {args.step}")
    run_step(args.step, batch=args.batch)
    log.info("Pipeline concluído.")
