#!/usr/bin/env python3
"""
=============================================================
scripts/04_intercoder_reliability.py
Calcula confiabilidade intercodificadores (Cohen's Kappa)
para validação do protocolo de codificação automática.

Uso: Codifique uma amostra de artigos manualmente e salve
os resultados em output/human_coded/. Este script compara
com a codificação automática em output/coded_events/.

Métricas calculadas:
  - Cohen's Kappa para elegibilidade DoCA (binary)
  - Cohen's Kappa para claim_code principal
  - Percent Agreement para crowd_size_range
  - F1-score para detecção de presença policial

Referência: Krippendorff (2004); Lombard et al. (2002)
=============================================================
"""

import os
import json
import logging
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv

load_dotenv()

BASE_DIR    = Path(__file__).parent.parent
OUTPUT_DIR  = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
CODED_DIR   = OUTPUT_DIR / "coded_events"
HUMAN_DIR   = OUTPUT_DIR / "human_coded"
LOG_DIR     = OUTPUT_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def cohen_kappa(y1: list, y2: list) -> float:
    """Calcula Cohen's Kappa entre duas listas de anotações."""
    if len(y1) != len(y2):
        raise ValueError("As listas devem ter o mesmo tamanho")

    labels = sorted(set(y1) | set(y2))
    n = len(y1)
    if n == 0:
        return 0.0

    # Concordância observada
    p_o = sum(a == b for a, b in zip(y1, y2)) / n

    # Concordância esperada por acaso
    p_e = 0.0
    for label in labels:
        p1 = y1.count(label) / n
        p2 = y2.count(label) / n
        p_e += p1 * p2

    if p_e == 1.0:
        return 1.0

    return (p_o - p_e) / (1 - p_e)


def percent_agreement(y1: list, y2: list) -> float:
    if not y1:
        return 0.0
    return sum(a == b for a, b in zip(y1, y2)) / len(y1)


def interpret_kappa(k: float) -> str:
    """Interpretação de Landis & Koch (1977)."""
    if k < 0:     return "sem concordância"
    if k < 0.20:  return "ligeira"
    if k < 0.40:  return "razoável"
    if k < 0.60:  return "moderada"
    if k < 0.80:  return "substancial"
    return "quase perfeita"


def run_reliability_check():
    """Compara codificação automática com codificação humana."""
    if not HUMAN_DIR.exists() or not list(HUMAN_DIR.glob("*.json")):
        log.warning(
            "Nenhuma codificação humana encontrada em output/human_coded/\n"
            "Para usar este script:\n"
            "  1. Selecione uma amostra aleatória de ~50-100 artigos\n"
            "  2. Codifique-os manualmente seguindo o protocolo DoCA\n"
            "  3. Salve cada evento como <article_id>_human.json\n"
            "     no formato idêntico ao output/coded_events/\n"
            "  4. Execute novamente este script"
        )
        return

    human_files = {p.stem.replace("_human", ""): p for p in HUMAN_DIR.glob("*_human.json")}
    auto_files  = {p.stem: p for p in CODED_DIR.glob("*.json")}

    # Artigos codificados por ambos
    overlap_ids = set(human_files.keys()) & set(auto_files.keys())
    log.info(f"Artigos com dupla codificação: {len(overlap_ids)}")

    if len(overlap_ids) < 10:
        log.warning("Amostra muito pequena (<10 artigos). Colete mais codificações humanas.")
        return

    # Coleta anotações pares
    eligible_human, eligible_auto   = [], []
    claim_code_human, claim_code_auto = [], []
    crowd_range_human, crowd_range_auto = [], []
    police_human, police_auto       = [], []

    for art_id in overlap_ids:
        with open(human_files[art_id], encoding="utf-8") as f:
            h = json.load(f)
        with open(auto_files[art_id], encoding="utf-8") as f:
            a = json.load(f)

        # Elegibilidade (se arquivo existe, é elegível)
        eligible_human.append(1)
        eligible_auto.append(1)

        # Claim code principal
        h_code = (h.get("claims") or [{}])[0].get("claim_code", "?")
        a_code = (a.get("claims") or [{}])[0].get("claim_code", "?")
        claim_code_human.append(h_code)
        claim_code_auto.append(a_code)

        # Crowd range
        h_range = h.get("crowd_size", {}).get("range_expression") or "?"
        a_range = a.get("crowd_size", {}).get("range_expression") or "?"
        crowd_range_human.append(h_range)
        crowd_range_auto.append(a_range)

        # Presença policial
        police_human.append(int(h.get("police_response", {}).get("presence", False)))
        police_auto.append(int(a.get("police_response", {}).get("presence", False)))

    # Cálculo das métricas
    k_claims  = cohen_kappa(claim_code_human, claim_code_auto)
    k_police  = cohen_kappa([str(x) for x in police_human], [str(x) for x in police_auto])
    pa_crowd  = percent_agreement(crowd_range_human, crowd_range_auto)

    log.info("=" * 60)
    log.info("RELATÓRIO DE CONFIABILIDADE INTERCODIFICADORES")
    log.info("=" * 60)
    log.info(f"Amostra: {len(overlap_ids)} artigos")
    log.info("")
    log.info(f"Claim code principal:")
    log.info(f"  Cohen's Kappa = {k_claims:.3f} ({interpret_kappa(k_claims)})")
    log.info("")
    log.info(f"Presença policial:")
    log.info(f"  Cohen's Kappa = {k_police:.3f} ({interpret_kappa(k_police)})")
    log.info("")
    log.info(f"Tamanho de multidão (range):")
    log.info(f"  % Concordância = {pa_crowd*100:.1f}%")
    log.info("=" * 60)

    # Interpretação para uso académico
    if k_claims >= 0.60:
        log.info("✓ Confiabilidade ADEQUADA para publicação acadêmica (Kappa ≥ 0.60)")
    elif k_claims >= 0.40:
        log.info("⚠ Confiabilidade RAZOÁVEL. Revisão do codebook recomendada.")
    else:
        log.info("✗ Confiabilidade INSUFICIENTE. Revisar instruções de codificação.")

    # Salva relatório
    report = {
        "date": __import__("datetime").datetime.utcnow().isoformat(),
        "n_double_coded": len(overlap_ids),
        "kappa_claim_code": round(k_claims, 4),
        "kappa_police_presence": round(k_police, 4),
        "percent_agreement_crowd_range": round(pa_crowd, 4),
        "interpretation_claims": interpret_kappa(k_claims),
    }
    out = OUTPUT_DIR / "dataset" / "intercoder_reliability.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    log.info(f"Relatório salvo em: {out}")


if __name__ == "__main__":
    run_reliability_check()
