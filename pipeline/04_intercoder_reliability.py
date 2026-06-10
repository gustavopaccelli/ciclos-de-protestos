"""04_intercoder_reliability.py — Confiabilidade intercodificadores.

Compara a codificação automática (pipeline/data/coded/) com uma codificação
manual de uma amostra (CSV com colunas event_id + variáveis categóricas) e
calcula Cohen's Kappa por variável.

Uso:
  python 04_intercoder_reliability.py amostra_manual.csv

O CSV manual deve conter event_id e ao menos uma das colunas:
claim_code, repertoire, crowd_size_scale, repression, eligible.
"""

import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

BASE = Path(__file__).resolve().parent
CODED_DIR = BASE / "data" / "coded"

CATEGORICAL = ["claim_code", "repertoire", "crowd_size_scale", "repression", "eligible"]


def load_auto() -> pd.DataFrame:
    rows = []
    for path in CODED_DIR.glob("*.json"):
        rows.extend(json.loads(path.read_text()).get("events", []))
    return pd.DataFrame(rows).set_index("event_id")


def main(manual_csv: str) -> None:
    manual = pd.read_csv(manual_csv, dtype=str).set_index("event_id")
    auto = load_auto()
    common = manual.index.intersection(auto.index)
    if len(common) == 0:
        raise SystemExit("Nenhum event_id em comum entre manual e automático.")
    print(f"{len(common)} eventos em comum\n")
    print(f"{'variável':<20}{'kappa':>8}{'n':>6}")
    for var in CATEGORICAL:
        if var not in manual.columns:
            continue
        a = auto.loc[common, var].astype(str)
        m = manual.loc[common, var].astype(str)
        mask = m.notna() & a.notna()
        kappa = cohen_kappa_score(m[mask], a[mask])
        print(f"{var:<20}{kappa:>8.3f}{mask.sum():>6}")
    print("\nInterpretação (Landis & Koch): <0.40 fraco | 0.41-0.60 moderado | "
          "0.61-0.80 substancial | >0.80 quase perfeito")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
