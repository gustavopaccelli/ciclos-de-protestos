"""03_build_dataset.py — Consolida eventos codificados em protest_events.

Lê pipeline/data/coded/*.json, desduplica (event_id e heurística
data+cidade+repertório+claim), valida e exporta:
  - data/protest_events.csv
  - data/protest_events.xlsx (4 abas: eventos, agregação anual,
    frequência de claims, distribuição geográfica)
"""

import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
CODED_DIR = BASE / "data" / "coded"
OUT_DIR = BASE.parent / "data"


def load_events() -> pd.DataFrame:
    rows = []
    for path in sorted(CODED_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        rows.extend(data.get("events", []))
    if not rows:
        raise SystemExit("Nenhum evento codificado em pipeline/data/coded/")
    return pd.DataFrame(rows)


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["event_id"])
    # mesmo evento coberto por mais de uma matéria
    key = ["event_date", "location_city", "repertoire", "claim_code"]
    df = df.sort_values("source_date").drop_duplicates(subset=key, keep="first")
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    n_nodate = df["event_date"].isna().sum()
    if n_nodate:
        print(f"[aviso] {n_nodate} eventos sem data — mantidos, revisar manualmente")
    return df


def export(df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / "protest_events.csv", index=False)

    eligible = df[df["eligible"] == True].copy()  # noqa: E712
    eligible["year"] = eligible["event_date"].dt.year

    with pd.ExcelWriter(OUT_DIR / "protest_events.xlsx", engine="xlsxwriter") as xw:
        df.to_excel(xw, sheet_name="protest_events", index=False)
        (eligible.groupby("year").size().rename("n_eventos")
            .to_frame().to_excel(xw, sheet_name="agregacao_anual"))
        (eligible.groupby(["claim_code", "claim_text"]).size()
            .rename("n").sort_values(ascending=False).head(200)
            .to_frame().to_excel(xw, sheet_name="frequencia_claims"))
        (eligible.groupby(["location_state", "location_city"]).size()
            .rename("n").sort_values(ascending=False)
            .to_frame().to_excel(xw, sheet_name="distribuicao_geografica"))

    print(f"{len(df)} eventos ({len(eligible)} elegíveis) → "
          f"{OUT_DIR/'protest_events.csv'} e .xlsx")


if __name__ == "__main__":
    export(validate(dedupe(load_events())))
