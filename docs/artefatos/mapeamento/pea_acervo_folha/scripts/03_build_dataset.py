#!/usr/bin/env python3
"""
=============================================================
scripts/03_build_dataset.py
Consolida todos os eventos codificados em um único dataset
CSV/XLSX e gera estatísticas de validação.

Saídas:
  output/dataset/pea_brasil_eventos.csv
  output/dataset/pea_brasil_eventos.xlsx
  output/dataset/validation_report.json
=============================================================
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_DIR    = Path(__file__).parent.parent
OUTPUT_DIR  = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
CODED_DIR   = OUTPUT_DIR / "coded_events"
DATASET_DIR = OUTPUT_DIR / "dataset"
LOG_DIR     = OUTPUT_DIR / "logs"

DATASET_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "build_dataset.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Normalização / achatamento do JSON aninhado
# ─────────────────────────────────────────────────────────────

def flatten_event(ev: dict) -> dict:
    """
    Converte o JSON hierárquico de um evento para uma linha plana
    adequada para CSV/DataFrame. Claims são serializados como strings
    separadas por " | " para manter legibilidade.
    """
    loc   = ev.get("location", {})
    crowd = ev.get("crowd_size", {})
    pol   = ev.get("police_response", {})
    cons  = ev.get("consequences", {})
    meta  = ev.get("_meta", {})

    # Serializa claims como "CODE:VALENCE:DESCRIPTION | ..."
    claims_str = " | ".join(
        f"{c.get('claim_code','?')}:{c.get('valence','?')}:{c.get('description','')}"
        for c in ev.get("claims", [])
    )
    # Extrai apenas os claim_codes para análise quantitativa
    claim_codes_str = "; ".join(c.get("claim_code", "?") for c in ev.get("claims", []))

    return {
        # Identificação
        "event_id":           ev.get("event_id", ""),
        "date":               ev.get("date", ""),
        "year":               ev.get("date", "0000")[:4],
        "month":              ev.get("date", "0000-00")[:7],

        # Localização
        "city":               loc.get("city", ""),
        "state":              loc.get("state", ""),

        # Atores
        "actors":             "; ".join(ev.get("actors", [])),
        "actor_primary":      ev.get("actors", [""])[0],
        "targets":            "; ".join(ev.get("targets", [])),

        # Demandas
        "claims_full":        claims_str,
        "claim_codes":        claim_codes_str,
        "n_claims":           len(ev.get("claims", [])),

        # Tamanho
        "crowd_exact":        crowd.get("exact_count"),
        "crowd_range":        crowd.get("range_expression"),

        # Polícia
        "police_presence":    pol.get("presence", False),
        "police_tactics":     "; ".join(pol.get("tactics", [])),
        "police_equipment":   "; ".join(pol.get("coercive_equipment", [])),

        # Consequências
        "arrests":            cons.get("arrests_count"),
        "injuries_protesters": cons.get("injuries_protesters"),
        "injuries_police":    cons.get("injuries_police"),
        "fatalities":         cons.get("fatalities"),
        "property_damage":    cons.get("property_damage", False),

        # Metadados da codificação
        "source_article_id":  meta.get("source_article_id", ""),
        "source_url":         meta.get("source_url", ""),
        "pub_date":           meta.get("pub_date", ""),
        "confidence":         meta.get("confidence", ""),
        "coder_model":        meta.get("coder_model", ""),
        "coded_at":           meta.get("coded_at", ""),
    }


# ─────────────────────────────────────────────────────────────
# Validação e relatório
# ─────────────────────────────────────────────────────────────

def validate_event(ev: dict) -> list[str]:
    """Retorna lista de avisos de validação para um evento."""
    warnings = []

    if not ev.get("date") or len(ev.get("date", "")) != 10:
        warnings.append("date_format_invalid")

    loc = ev.get("location", {})
    if not loc.get("city"):
        warnings.append("city_missing")
    if not loc.get("state") or len(loc.get("state", "")) != 2:
        warnings.append("state_invalid")

    if not ev.get("actors"):
        warnings.append("actors_empty")

    if not ev.get("claims"):
        warnings.append("claims_empty")
    else:
        for c in ev["claims"]:
            if not c.get("claim_code") or len(c.get("claim_code", "")) != 4:
                warnings.append("claim_code_invalid")
                break
            if c.get("valence") not in ("01", "02", "03"):
                warnings.append("valence_invalid")
                break

    crowd = ev.get("crowd_size", {})
    if crowd.get("exact_count") is None and crowd.get("range_expression") is None:
        warnings.append("crowd_size_missing")

    return warnings


def build_validation_report(events: list[dict]) -> dict:
    """Gera relatório de validação do dataset."""
    total = len(events)
    warnings_counter = Counter()
    events_with_warnings = 0
    year_counter = Counter()
    state_counter = Counter()
    claim_counter = Counter()

    for ev in events:
        w = validate_event(ev)
        if w:
            events_with_warnings += 1
            warnings_counter.update(w)

        year = ev.get("date", "0000")[:4]
        year_counter[year] += 1

        state = ev.get("location", {}).get("state", "??")
        state_counter[state] += 1

        for c in ev.get("claims", []):
            claim_counter[c.get("claim_code", "?")] += 1

    return {
        "generated_at":          datetime.utcnow().isoformat(),
        "total_events":          total,
        "events_with_warnings":  events_with_warnings,
        "data_quality_pct":      round((1 - events_with_warnings / max(total, 1)) * 100, 1),
        "warnings_breakdown":    dict(warnings_counter.most_common()),
        "events_by_year":        dict(sorted(year_counter.items())),
        "events_by_state":       dict(state_counter.most_common(10)),
        "top_claim_codes":       dict(claim_counter.most_common(15)),
    }


# ─────────────────────────────────────────────────────────────
# Deduplicação pós-codificação
# ─────────────────────────────────────────────────────────────

def deduplicate(events: list[dict]) -> list[dict]:
    """
    Remove eventos duplicados com base no event_id.
    Em caso de duplicata (mesmo ID gerado por artigos diferentes que
    cobrem o mesmo evento), mantém o de maior confidence.
    """
    seen = {}
    conf_order = {"high": 3, "medium": 2, "low": 1, "": 0}

    for ev in events:
        eid = ev.get("event_id", "")
        if eid not in seen:
            seen[eid] = ev
        else:
            existing_conf = conf_order.get(seen[eid].get("_meta", {}).get("confidence", ""), 0)
            new_conf      = conf_order.get(ev.get("_meta", {}).get("confidence", ""), 0)
            if new_conf > existing_conf:
                seen[eid] = ev

    unique = list(seen.values())
    log.info(f"Deduplicação: {len(events)} → {len(unique)} eventos únicos")
    return unique


# ─────────────────────────────────────────────────────────────
# Construção do dataset principal
# ─────────────────────────────────────────────────────────────

def build_dataset():
    event_files = sorted(CODED_DIR.glob("*.json"))
    log.info(f"Carregando {len(event_files)} arquivos de eventos codificados...")

    events_raw = []
    for path in event_files:
        try:
            with open(path, encoding="utf-8") as f:
                ev = json.load(f)
            events_raw.append(ev)
        except Exception as e:
            log.warning(f"Erro ao carregar {path.name}: {e}")

    if not events_raw:
        log.error("Nenhum evento codificado encontrado em output/coded_events/")
        return

    # Deduplicação
    events = deduplicate(events_raw)

    # Validação
    report = build_validation_report(events)
    log.info(f"Qualidade dos dados: {report['data_quality_pct']}% sem avisos")
    log.info(f"Top claim codes: {list(report['top_claim_codes'].items())[:5]}")

    report_path = DATASET_DIR / "validation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    log.info(f"Relatório de validação salvo em: {report_path}")

    # Achatamento para DataFrame
    rows = [flatten_event(ev) for ev in events]
    df = pd.DataFrame(rows)

    # Ordenação por data
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # --- CSV ---
    csv_path = DATASET_DIR / "pea_brasil_eventos.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    log.info(f"CSV salvo: {csv_path}  ({len(df)} linhas)")

    # --- XLSX com múltiplas abas ---
    xlsx_path = DATASET_DIR / "pea_brasil_eventos.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        # Aba principal
        df.to_excel(writer, sheet_name="eventos", index=False)

        # Aba de estatísticas por ano
        year_stats = df.groupby("year").agg(
            n_eventos       = ("event_id", "count"),
            n_com_policia   = ("police_presence", "sum"),
            n_com_prisoes   = ("arrests", lambda x: (x > 0).sum()),
            n_com_feridos   = ("injuries_protesters", lambda x: (x > 0).sum()),
            n_estados_únicos = ("state", "nunique"),
        ).reset_index()
        year_stats.to_excel(writer, sheet_name="por_ano", index=False)

        # Aba de claims mais frequentes
        all_claims = []
        for _, row in df.iterrows():
            for code in str(row.get("claim_codes", "")).split(";"):
                c = code.strip()
                if c and c != "?":
                    all_claims.append({"claim_code": c, "year": row.get("year", "")})
        if all_claims:
            claims_df = pd.DataFrame(all_claims)
            claims_freq = claims_df.groupby("claim_code").size().reset_index(name="frequencia")
            claims_freq = claims_freq.sort_values("frequencia", ascending=False)
            claims_freq.to_excel(writer, sheet_name="frequencia_claims", index=False)

        # Aba de distribuição geográfica
        geo_stats = df.groupby(["state", "city"]).size().reset_index(name="n_eventos")
        geo_stats = geo_stats.sort_values("n_eventos", ascending=False)
        geo_stats.to_excel(writer, sheet_name="distribuicao_geografica", index=False)

    log.info(f"XLSX salvo: {xlsx_path}")
    log.info("─" * 60)
    log.info(f"Dataset final: {len(df)} eventos | {df['year'].nunique()} anos | {df['state'].nunique()} estados")


if __name__ == "__main__":
    build_dataset()
