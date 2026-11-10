"""intercoder_reliability.py — Confiabilidade intercodificadores (AEP-BR).

Passagem 5 do protocolo (docs/aep-protocol-bep.md §11). Compara a codificação
automática (bancos/03_aep_br/codificacao/) com a codificação manual de uma amostra e
calcula Cohen's Kappa por variável.

Também grava o registro obrigatório do protocolo §12.6 (--relatorio): modelo e
versão do prompt das codificações comparadas, tamanho e composição do gold
standard, κ por variável e a tipologia de erro do §12.4 (elegibilidade,
unitização, categorização, extração numérica e a parte detectável de alucinação).

Uso:
  python src/preprocessing/intercoder_reliability.py bancos/03_aep_br/validacao/amostra_manual.csv \
      --out bancos/03_aep_br/validacao/kappa_<data>.csv \
      --relatorio bancos/03_aep_br/validacao/validation_report_<data>.json

O CSV manual deve conter evento_id e ao menos uma das variáveis categóricas
listadas em CATEGORICAL (lidas do codebook AEP-BR). Variáveis ausentes do CSV
são ignoradas. Em variáveis de lista (tema_codigo, repertorio, alvo,
resposta_estatal) compara-se o primeiro elemento, isto é, o principal; no CSV
manual a lista vem separada por ";".
"""

import argparse
import datetime as dt
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

CODED_DIR = paths.AEP_CODIFICACAO
KAPPA_MIN = cb.limiar_kappa()

# Variáveis categóricas aferidas: todas as de vocabulário fechado e as booleanas,
# exceto as atribuídas pelo pipeline (não há o que comparar) e as de qualidade
# da fonte.
_FORA = cb.CAMPOS_PIPELINE | {"qualidade_ocr", "confianca"}
EXPERIMENTAIS = set(cb.experimentais())
# Indicadores comparáveis das variáveis experimentais que são listas de objetos
# (bloco X): o codificador manual preenche estas colunas; do lado automático
# elas são derivadas das listas por derivar_experimentais().
DERIVADAS = {
    "aliado_presente": "bool", "aliado_tipo_principal": "str",
    "reacao_apoio": "bool", "reacao_rejeicao": "bool",
}
BOOL_FIELDS = (set(cb.nomes("bool")) - _FORA) | {k for k, t in DERIVADAS.items() if t == "bool"}
CATEGORICAL = [n for n in cb.nomes()
               if n not in _FORA and n not in EXPERIMENTAIS
               and (n in cb.campos_enum() or n in BOOL_FIELDS)]
CATEGORICAL_X = [n for n in cb.experimentais() if n in cb.campos_enum()] + list(DERIVADAS)
LIST_FIELDS = set(cb.campos_lista())
# Contagens comparadas por igualdade (extração numérica, §12.4). Na planilha
# manual: vazio = não codificado; "NA" = a matéria não menciona; -1 = houve, sem número.
NUMERICAS = ["publico_max", "detidos", "feridos", "mortos"]
# Colunas que o codificador humano preenche na planilha do gold standard.
COLUNAS_MANUAIS = CATEGORICAL + CATEGORICAL_X + NUMERICAS

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


def derivar_experimentais(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma as listas de objetos do bloco X em indicadores comparáveis."""
    def lista(v):
        return v if isinstance(v, list) else []
    if "aliados_institucionais" in df.columns:
        al = df["aliados_institucionais"].map(lista)
        df["aliado_presente"] = al.map(bool)
        df["aliado_tipo_principal"] = al.map(lambda v: v[0].get("tipo") if v else "nenhum")
    if "reacoes_publicas" in df.columns:
        re_ = df["reacoes_publicas"].map(lista)
        df["reacao_apoio"] = re_.map(lambda v: any(r.get("sinal") == "apoio" for r in v))
        df["reacao_rejeicao"] = re_.map(lambda v: any(r.get("sinal") == "rejeicao" for r in v))
    return df


def load_auto() -> pd.DataFrame:
    rows = []
    for path in CODED_DIR.glob("*.json"):
        for ev in json.loads(path.read_text()).get("eventos", []):
            rows.append({**ev, "arquivo": path.name})
    if not rows:
        raise SystemExit("Nenhum evento codificado em bancos/03_aep_br/codificacao/")
    return derivar_experimentais(pd.DataFrame(rows)).set_index("evento_id")


def _num(v):
    """Contagem canônica: None = não menciona; int caso contrário."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip().lower()
    if s in ("", "na", "null", "none", "nan"):
        return None
    return int(float(s))


def _numericas(manual, auto, common) -> tuple[dict, int]:
    """Discordâncias de extração numérica e valores que só o LLM viu (possível alucinação)."""
    saida, alucinacao = {}, 0
    for var in NUMERICAS:
        if var not in manual.columns or var not in auto.columns:
            continue
        preenchidos = [i for i in common if str(manual.at[i, var] or "").strip() not in ("", "nan")]
        pares = [(_num(manual.at[i, var]), _num(auto.at[i, var])) for i in preenchidos]
        saida[var] = {"comparados": len(pares), "discordancias": sum(m != a for m, a in pares)}
        alucinacao += sum(m is None and a is not None for m, a in pares)
    return saida, alucinacao


def _elegibilidade(manual, auto, common) -> dict:
    if "elegivel" not in manual.columns:
        return {}
    m = manual.loc[common, "elegivel"].map(lambda v: canon(v, True))
    a = auto.loc[common, "elegivel"].map(lambda v: canon(v, True))
    return {"falso_positivo": int(((a == "True") & (m == "False")).sum()),
            "falso_negativo": int(((a == "False") & (m == "True")).sum())}


def relatorio(manual_csv, manual, auto, common, so_manual, so_auto, linhas) -> dict:
    """Registro obrigatório do protocolo §12.6."""
    comp = auto.loc[common]
    contagem = lambda col: {str(k): int(v) for k, v in comp[col].fillna("sem_fase").value_counts().items()} \
        if col in comp.columns else {}
    numericas, alucinacao = _numericas(manual, auto, common)
    reprovadas = [r["variavel"] for r in linhas if r["situacao"] == "ABAIXO DO LIMIAR"]
    return {
        "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "codebook_versao": cb.aep()["versao"],
        "codificacao_automatica": {
            "modelo_e_prompt": {str(k): int(v) for k, v in comp["modelo_versao"].value_counts().items()}
            if "modelo_versao" in comp.columns else {},
            "registros_de_execucao": "bancos/03_aep_br/validacao/execucoes/ (mesmo prompt_hash)",
        },
        "gold_standard": {
            "arquivo": str(manual_csv),
            "materias": int(manual["arquivo"].nunique()) if "arquivo" in manual.columns else None,
            "eventos_comparados": len(common),
            "composicao_por_ciclo": contagem("ciclo"),
            "composicao_por_fase": contagem("fase"),
        },
        "kappa_minimo": KAPPA_MIN,
        "kappa": [{**r, "kappa": None if pd.isna(r["kappa"]) else round(float(r["kappa"]), 3)} for r in linhas],
        "tipologia_erros": {
            "elegibilidade": _elegibilidade(manual, auto, common),
            "unitizacao": {"so_manual": so_manual, "so_automatico": so_auto},
            "categorizacao": {r["variavel"]: r["discordancias"] for r in linhas if r["variavel"] != "elegivel"},
            "extracao_numerica": numericas,
            "alucinacao": {
                "contagens_sem_base_no_texto": alucinacao,
                "nota": "Só detecta número que o LLM registrou onde o codificador humano marcou NA; "
                        "outros casos de informação inventada exigem revisão humana dos registros.",
            },
        },
        "decisao_12_5": {
            "abaixo_do_limiar": reprovadas,
            "proximo_passo": "codificação aceita" if not reprovadas else
                             "revisar o prompt nos pontos indicados e medir de novo no mesmo gold standard",
        },
    }


def main(manual_csv: str, out_csv: str | None, relatorio_json: str | None = None) -> None:
    # keep_default_na=False: "NA" na planilha significa "a matéria não menciona" e não pode virar célula vazia.
    manual = pd.read_csv(manual_csv, dtype=str, keep_default_na=False)
    auto = load_auto()
    if "arquivo" in manual.columns:
        # Piloto: compara só as matérias da planilha e mede a unitização.
        auto = auto[auto["arquivo"].isin(set(manual["arquivo"]))]
    manual = manual[manual["evento_id"].fillna("").str.strip() != ""].set_index("evento_id")
    common = manual.index.intersection(auto.index)
    if len(common) == 0:
        raise SystemExit("Nenhum evento_id em comum entre manual e automático.")
    so_manual, so_auto = len(manual.index.difference(auto.index)), len(auto.index.difference(manual.index))
    print(f"Unitização: {len(common)} eventos em comum; {so_manual} só no manual "
          f"(o LLM não viu); {so_auto} só no automático (removidos na revisão manual).")
    print(f"Limiar do codebook: κ ≥ {KAPPA_MIN}\n")

    linhas = []
    for grupo, variaveis in (("nucleo", CATEGORICAL), ("experimental", CATEGORICAL_X)):
        print(f"[{grupo}]\n{'variável':<24}{'kappa':>8}{'n':>6}  situação")
        linhas += _kappas(grupo, variaveis, manual, auto, common)
        print()
    _rodape(linhas)

    if out_csv:
        pd.DataFrame(linhas).to_csv(out_csv, index=False)
        print(f"\nRelatório → {out_csv}")
    if relatorio_json:
        rel = relatorio(manual_csv, manual, auto, common, so_manual, so_auto, linhas)
        Path(relatorio_json).write_text(json.dumps(rel, ensure_ascii=False, indent=2))
        print(f"Registro §12.6 → {relatorio_json}")


def _kappas(grupo, variaveis, manual, auto, common) -> list[dict]:
    linhas = []
    for var in variaveis:
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
        linhas.append({"grupo": grupo, "variavel": var, "kappa": kappa,
                       "n": int(mask.sum()), "discordancias": int((m[mask] != a[mask]).sum()),
                       "situacao": situacao})
        print(f"{var:<24}{kappa:>8.3f}{mask.sum():>6}  {situacao}")
    return linhas


def _rodape(linhas: list[dict]) -> None:
    print("Padrão de confiabilidade (Krippendorff, 2018): >= 0.800 permite conclusões; "
          "0.667-0.799 apenas conclusões provisórias; abaixo de 0.667 não se conclui.")
    print(f"Ressalva: esse padrão é para o alpha de Krippendorff e aqui se calcula o kappa de "
          f"Cohen — o corte é aplicado por analogia. E o limiar do projeto (KAPPA_MIN = "
          f"{KAPPA_MIN}) fica entre os dois cortes: é escolha nossa, não parâmetro consagrado.")
    reprovadas = [r["variavel"] for r in linhas if r["situacao"] == "ABAIXO DO LIMIAR"]
    if reprovadas:
        print(f"\n[atenção] κ < {KAPPA_MIN} em: {', '.join(reprovadas)} — protocolo §11 "
              f"Passagem 5: revisar o prompt ou excluir a variável da análise.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("manual_csv", help="CSV da codificação manual da amostra")
    ap.add_argument("--out", default=None, help="grava o relatório de kappa em CSV")
    ap.add_argument("--relatorio", default=None, help="grava o registro §12.6 (validation_report) em JSON")
    args = ap.parse_args()
    main(args.manual_csv, args.out, args.relatorio)
