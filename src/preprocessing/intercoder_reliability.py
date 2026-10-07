"""intercoder_reliability.py — Confiabilidade intercodificadores (AEP-BR).

Passagem 5 do protocolo (docs/aep-protocol-bep.md §11). Compara a codificação
automática (data/interim/) com a codificação manual de uma amostra e
calcula Cohen's Kappa por variável.

Uso:
  python src/preprocessing/intercoder_reliability.py amostra_manual.csv [--out relatorio.csv]

O CSV manual deve conter evento_id e ao menos uma das variáveis categóricas
listadas em CATEGORICAL (lidas do codebook AEP-BR). Variáveis ausentes do CSV
são ignoradas. Em variáveis de lista (tema_codigo, repertorio, alvo,
resposta_estatal) compara-se o primeiro elemento, isto é, o principal; no CSV
manual a lista vem separada por ";".
"""

import argparse
import json
import unicodedata
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aep_codebook as cb  # noqa: E402

import pandas as pd
from sklearn.metrics import cohen_kappa_score

CODED_DIR = paths.INTERIM
KAPPA_MIN = cb.limiar_kappa()

# Variáveis categóricas aferidas: todas as de vocabulário fechado e as booleanas,
# exceto as atribuídas pelo pipeline (não há o que comparar) e as de qualidade
# da fonte.
_FORA = cb.CAMPOS_PIPELINE | {"qualidade_ocr", "confianca"}
BOOL_FIELDS = set(cb.nomes("bool")) - _FORA
CATEGORICAL = [n for n in cb.nomes()
               if n not in _FORA and (n in cb.campos_enum() or n in BOOL_FIELDS)]
LIST_FIELDS = set(cb.campos_lista())

_TRUTHY = {"true", "1", "sim", "yes", "verdadeiro"}
_FALSY = {"false", "0", "nao", "no", "falso"}


def _slug(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().split())


def principal(value):
    """Primeiro elemento de uma lista (JSON) ou de 'a; b' (CSV manual)."""
    if isinstance(value, list):
        return value[0] if value else None
    if isinstance(value, str):
        return value.split(";")[0].strip() or None
    return value


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
        rows.extend(json.loads(path.read_text()).get("eventos", []))
    if not rows:
        raise SystemExit("Nenhum evento codificado em data/interim/")
    return pd.DataFrame(rows).set_index("evento_id")


def main(manual_csv: str, out_csv: str | None) -> None:
    manual = pd.read_csv(manual_csv, dtype=str).set_index("evento_id")
    auto = load_auto()
    common = manual.index.intersection(auto.index)
    if len(common) == 0:
        raise SystemExit("Nenhum evento_id em comum entre manual e automático.")
    print(f"{len(common)} eventos em comum (limiar do codebook: κ ≥ {KAPPA_MIN})\n")

    linhas = []
    print(f"{'variável':<24}{'kappa':>8}{'n':>6}  situação")
    for var in CATEGORICAL:
        if var not in manual.columns or var not in auto.columns:
            continue
        is_bool = var in BOOL_FIELDS
        prep = principal if var in LIST_FIELDS else (lambda v: v)
        a = auto.loc[common, var].map(lambda v: canon(prep(v), is_bool))
        m = manual.loc[common, var].map(lambda v: canon(prep(v), is_bool))
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

    print("\nPadrão de confiabilidade (Krippendorff, 2018): >= 0.800 permite conclusões; "
          "0.667-0.799 apenas conclusões provisórias; abaixo de 0.667 não se conclui.")
    print(f"Ressalva: esse padrão é para o alpha de Krippendorff e aqui se calcula o kappa de "
          f"Cohen — o corte é aplicado por analogia. E o limiar do projeto (KAPPA_MIN = "
          f"{KAPPA_MIN}) fica entre os dois cortes: é escolha nossa, não parâmetro consagrado.")
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
