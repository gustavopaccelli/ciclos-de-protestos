"""04_intercoder_reliability.py — Confiabilidade intercodificadores.

Passagem 5 do protocolo (docs/aep-protocol-bep.md §11). Compara a codificação
automática (pipeline/data/coded/) com a codificação manual de uma amostra e
calcula Cohen's Kappa por variável.

Uso:
  python 04_intercoder_reliability.py amostra_manual.csv [--out relatorio.csv]

O CSV manual deve conter event_id e ao menos uma das variáveis categóricas
listadas em CATEGORICAL. Variáveis ausentes do CSV são ignoradas.
"""

import argparse
import json
import unicodedata
from pathlib import Path

import pandas as pd
import yaml
from sklearn.metrics import cohen_kappa_score

BASE = Path(__file__).resolve().parent
CODED_DIR = BASE / "data" / "coded"
CODEBOOK = yaml.safe_load((BASE / "config" / "doca_codebook.yaml").read_text())
KAPPA_MIN = CODEBOOK.get("intercoder_kappa_threshold", 0.75)

# Cobertura ampliada: antes só 5 variáveis eram aferidas, das ~40 do codebook.
CATEGORICAL = [
    # Bloco I
    "location_venue_type", "location_conventional", "city_size",
    "crowd_size_scale", "crowd_size_bep",
    # Bloco III
    "repertoire",
    # Bloco IV
    "claim_code", "valence",
    # Bloco V
    "conflict_present", "repression", "conflict_police", "conflict_inter_group",
    # Elegibilidade e MPEDS
    "eligible", "multi_event_article", "counter_protest", "target",
]

BOOL_FIELDS = {
    "eligible", "conflict_present", "conflict_police", "conflict_inter_group",
    "multi_event_article", "counter_protest", "location_conventional",
}

_TRUTHY = {"true", "1", "sim", "yes", "verdadeiro"}
_FALSY = {"false", "0", "nao", "no", "falso"}


def _slug(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().split())


def canon(value, is_bool: bool) -> str:
    """Forma canônica comparável entre os dois lados.

    Sem isto, `eligible` do lado manual chega como "TRUE"/"true"/"1" (CSV lido
    como str) e do lado automático como o bool Python estringado "True" — o
    kappa resultante era quase sem sentido.
    """
    s = _slug(value)
    if not s:
        return ""
    if is_bool:
        if s in _TRUTHY:
            return "True"
        if s in _FALSY:
            return "False"
    return s


def load_auto() -> pd.DataFrame:
    rows = []
    for path in CODED_DIR.glob("*.json"):
        rows.extend(json.loads(path.read_text()).get("events", []))
    if not rows:
        raise SystemExit("Nenhum evento codificado em pipeline/data/coded/")
    return pd.DataFrame(rows).set_index("event_id")


def main(manual_csv: str, out_csv: str | None) -> None:
    manual = pd.read_csv(manual_csv, dtype=str).set_index("event_id")
    auto = load_auto()
    common = manual.index.intersection(auto.index)
    if len(common) == 0:
        raise SystemExit("Nenhum event_id em comum entre manual e automático.")
    print(f"{len(common)} eventos em comum (limiar do codebook: κ ≥ {KAPPA_MIN})\n")

    linhas = []
    print(f"{'variável':<24}{'kappa':>8}{'n':>6}  situação")
    for var in CATEGORICAL:
        if var not in manual.columns or var not in auto.columns:
            continue
        is_bool = var in BOOL_FIELDS
        a = auto.loc[common, var].map(lambda v: canon(v, is_bool))
        m = manual.loc[common, var].map(lambda v: canon(v, is_bool))
        mask = (a != "") & (m != "")
        if mask.sum() == 0:
            continue
        if m[mask].nunique() == 1 and a[mask].nunique() == 1 and (m[mask] == a[mask]).all():
            # Kappa é indefinido quando só há uma categoria observada; concordância total.
            kappa = float("nan")
            situacao = "categoria única (acordo total)"
        else:
            kappa = cohen_kappa_score(m[mask], a[mask])
            situacao = "OK" if kappa >= KAPPA_MIN else "ABAIXO DO LIMIAR"
        linhas.append({"variavel": var, "kappa": kappa,
                       "n": int(mask.sum()), "situacao": situacao})
        print(f"{var:<24}{kappa:>8.3f}{mask.sum():>6}  {situacao}")

    print("\nInterpretação (Landis & Koch): <0.40 fraco | 0.41-0.60 moderado | "
          "0.61-0.80 substancial | >0.80 quase perfeito")
    reprovadas = [r["variavel"] for r in linhas if r["situacao"] == "ABAIXO DO LIMIAR"]
    if reprovadas:
        print(f"\n[atenção] κ < {KAPPA_MIN} em: {', '.join(reprovadas)} — protocolo §11 "
              f"Passagem 5: revisar o prompt ou excluir a variável da análise.")

    if out_csv:
        pd.DataFrame(linhas).to_csv(out_csv, index=False)
        print(f"\nRelatório → {out_csv}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("manual_csv", help="CSV da codificação manual da amostra")
    ap.add_argument("--out", default=None, help="grava o relatório de kappa em CSV")
    args = ap.parse_args()
    main(args.manual_csv, args.out)
