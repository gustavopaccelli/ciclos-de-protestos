"""build_dataset.py — Consolida eventos codificados (AEP-BR) em protest_events.

Passagem 4 do protocolo (docs/aep-protocol-bep.md §11). Lê
data/interim/*.json, normaliza contra o codebook AEP-BR, atribui
`evento_canonico_id` e exporta:

  - data/processed/harmonizado/protest_events_raw.csv   (uma linha por EXTRAÇÃO, sem deduplicação)
  - data/processed/harmonizado/protest_events.csv       (uma linha por evento canônico)
  - data/processed/harmonizado/protest_events.xlsx      (4 abas: eventos, agregação anual,
                                   frequência de temas, distribuição geográfica)

O arquivo `_raw` é o registro auditável de tudo que foi extraído: sem ele não
há como reconstruir quantas fontes cobriram cada evento nem revisar decisões
de deduplicação.
"""

import json
import re
import unicodedata
import uuid
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aep_codebook as cb  # noqa: E402

import pandas as pd

CODED_DIR = paths.INTERIM
OUT_DIR = paths.PROCESSED / "harmonizado"

CANONICAL_NAMESPACE = uuid.UUID("7c0e4d9a-1984-1992-2013-201520160001")

# Campos com vocabulário fechado, booleanos e listas — todos lidos do codebook.
ENUM_FIELDS = cb.campos_enum()
BOOL_FIELDS = cb.nomes("bool")
LIST_FIELDS = cb.campos_lista()


def load_events() -> pd.DataFrame:
    rows = []
    for path in sorted(CODED_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        rows.extend(data.get("eventos", []))
    if not rows:
        raise SystemExit("Nenhum evento codificado em data/interim/")
    return pd.DataFrame(rows)


def _slug(value) -> str:
    """Normaliza texto para comparação: sem acento, sem caixa, sem espaço extra."""
    if pd.isna(value) or value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().split())


def coerce_bool(series: pd.Series) -> pd.Series:
    """Converte bool/str/int para booleano nullable.

    Necessário porque o mesmo campo chega como bool (JSON do coder) ou como
    string ("TRUE"/"true"/"1") quando revisado em planilha.
    """
    truthy = {"true", "1", "sim", "yes", "verdadeiro"}
    falsy = {"false", "0", "nao", "não", "no", "falso"}

    def conv(v):
        if isinstance(v, bool):
            return v
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return pd.NA
        s = _slug(v)
        if s in truthy:
            return True
        if s in falsy:
            return False
        return pd.NA

    return series.map(conv).astype("boolean")


MESES_PT = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}


def parse_data_ptbr(series) -> pd.Series:
    """Converte o date_hint do Acervo ('12.abr.1984') em datetime.

    pd.to_datetime sozinho parseia só os meses cujo abreviado coincide com o
    inglês (jan, mar, jun, jul, nov) e devolve NaT em fev/abr/mai/ago/set/out/
    dez. O resultado seria uma coluna de datas com lacuna SAZONAL — grave num
    corpus cujo pico (Diretas Já) está justamente em abril.
    """
    if series is None:
        return pd.Series(pd.NaT, dtype="datetime64[ns]")
    series = pd.Series(series)

    def conv(v):
        if not isinstance(v, str) or not v.strip():
            return pd.NaT
        m = re.search(r"(\d{1,2})[./-]\s*([a-zç]{3,})[./-]\s*(\d{4})",
                      v.strip().lower())
        if m and m.group(2)[:3] in MESES_PT:
            return pd.Timestamp(int(m.group(3)), MESES_PT[m.group(2)[:3]],
                                int(m.group(1)))
        return pd.to_datetime(v, errors="coerce", dayfirst=True)

    return pd.to_datetime(series.map(conv), errors="coerce")


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza contra o codebook e reporta valores fora do vocabulário.

    Antes esta etapa era apenas declarada no protocolo (§7/§11 Passagem 4) e
    nunca executada: o script sequer carregava o codebook.
    """
    for field in BOOL_FIELDS:
        if field in df.columns:
            df[field] = coerce_bool(df[field])

    for field, vocab in ENUM_FIELDS.items():
        if field not in df.columns:
            continue
        if field in LIST_FIELDS:
            observed = {x for lst in df[field].dropna() for x in (lst or [])}
        else:
            df[field] = df[field].map(lambda v: v.strip() if isinstance(v, str) else v)
            observed = set(df[field].dropna().unique())
        unknown = observed - vocab
        if unknown:
            print(f"[aviso] {field}: valores fora do codebook → {sorted(unknown)}")

    for field in ("cidade", "uf"):
        if field in df.columns:
            df[field] = df[field].map(lambda v: v.strip() if isinstance(v, str) else v)
    if "uf" in df.columns:
        df["uf"] = df["uf"].map(
            lambda v: v.upper() if isinstance(v, str) else v
        )

    df["data_inicio"] = pd.to_datetime(df["data_inicio"], errors="coerce")
    # Data da matéria mais antiga do registro, para ordenar no collapse().
    df["data_publicacao"] = parse_data_ptbr(df["fontes"].map(
        lambda fs: (fs or [{}])[0].get("data_publicacao") if isinstance(fs, list) else None))
    n_nodate = df["data_inicio"].isna().sum()
    if n_nodate:
        print(f"[aviso] {n_nodate} eventos sem data — mantidos, revisar manualmente")

    # Campos do pipeline ainda não preenchidos (evento_canonico_id vem depois,
    # cidade_ibge/porte_cidade na normalização geográfica) dariam aviso sempre.
    aferiveis = df.columns.difference(["evento_canonico_id", "cidade_ibge", "porte_cidade"])
    missing = df[aferiveis].isna().mean()
    limiar = cb.limiar_missing()
    acima = missing[missing > limiar]
    if len(acima):
        print(f"[aviso] variáveis com >{limiar:.0%} de ausência (protocolo §7): "
              f"{sorted(acima.index)}")
    return df


def assign_canonical(df: pd.DataFrame) -> pd.DataFrame:
    """Atribui evento_canonico_id — protocolo §10.3.

    Critério implementado: mesma data + mesma localidade (cidade+UF) + mesma
    demanda principal. É a versão determinística e auditável do critério do
    protocolo ("datas sobrepostas + localidade igual ou contígua + atores e
    demandas compatíveis").

    LIMITE CONHECIDO: não trata contiguidade geográfica (cidades vizinhas) nem
    sobreposição parcial de datas em eventos plurianuais. Casos assim continuam
    a exigir arbitragem do editor humano, conforme §10.3.
    """
    def key(row) -> str:
        date = row["data_inicio"]
        cidade = _slug(row.get("cidade"))
        # Chave incompleta NÃO agrupa: sem data ou sem cidade não há como
        # afirmar que duas extrações são o mesmo evento. Agrupá-las fundiria
        # eventos distintos que apenas compartilham lacunas — o próprio
        # evento_id vira a chave, e a extração é preservada para arbitragem
        # humana (§10.3).
        if pd.isna(date) or not cidade:
            return f"SEM-CHAVE|{row['evento_id']}"
        temas = row.get("tema_codigo")
        return "|".join([
            date.strftime("%Y-%m-%d"),
            cidade,
            _slug(row.get("uf")),
            str(temas[0]) if isinstance(temas, list) and temas else "",
        ])

    df["_canonical_key"] = df.apply(key, axis=1)
    df["evento_canonico_id"] = df["_canonical_key"].map(
        lambda k: str(uuid.uuid5(CANONICAL_NAMESPACE, k))
    )
    n_canon = df["evento_canonico_id"].nunique()
    n_sem_chave = int(df["_canonical_key"].str.startswith("SEM-CHAVE").sum())
    print(f"{len(df)} extrações → {n_canon} eventos canônicos")
    if n_sem_chave:
        print(f"[aviso] {n_sem_chave} extrações sem data e/ou sem cidade não "
              "foram agrupadas (chave incompleta) — conferir manualmente")
    return df


def collapse(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por evento canônico, mantendo a extração da matéria mais antiga.

    A ordenação usa data_publicacao já convertida para datetime — antes era uma
    string não parseada, o que ordenava lexicograficamente.
    """
    df = df.drop_duplicates(subset=["evento_id"])
    n_fontes = df.groupby("evento_canonico_id").size().rename("n_extracoes")
    out = (df.sort_values("data_publicacao", na_position="last")
             .drop_duplicates(subset=["evento_canonico_id"], keep="first")
             .merge(n_fontes, left_on="evento_canonico_id", right_index=True))
    return out.drop(columns=["_canonical_key"], errors="ignore")


def para_planilha(df: pd.DataFrame) -> pd.DataFrame:
    """Listas de texto viram 'a; b'; listas de objetos viram JSON."""
    out = df.copy()
    for field in LIST_FIELDS:
        if field not in out.columns:
            continue
        def conv(v):
            if not isinstance(v, list):
                return v
            if any(isinstance(x, dict) for x in v):
                return json.dumps(v, ensure_ascii=False)
            return "; ".join(str(x) for x in v)
        out[field] = out[field].map(conv)
    return out


def export(raw: pd.DataFrame, df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    para_planilha(raw.drop(columns=["_canonical_key"], errors="ignore")).to_csv(
        OUT_DIR / "protest_events_raw.csv", index=False
    )
    eligible = df[df["elegivel"].fillna(False)].copy()
    eligible["ano"] = eligible["data_inicio"].dt.year
    eligible["tema_principal"] = eligible["tema_codigo"].map(
        lambda v: v[0] if isinstance(v, list) and v else None)
    df = para_planilha(df)
    df.to_csv(OUT_DIR / "protest_events.csv", index=False)

    with pd.ExcelWriter(OUT_DIR / "protest_events.xlsx", engine="xlsxwriter") as xw:
        df.to_excel(xw, sheet_name="protest_events", index=False)
        (eligible.groupby("ano").size().rename("n_eventos")
            .to_frame().to_excel(xw, sheet_name="agregacao_anual"))
        (eligible.groupby(["tema_principal", "tema_texto"]).size()
            .rename("n").sort_values(ascending=False).head(200)
            .to_frame().to_excel(xw, sheet_name="frequencia_temas"))
        (eligible.groupby(["uf", "cidade"]).size()
            .rename("n").sort_values(ascending=False)
            .to_frame().to_excel(xw, sheet_name="distribuicao_geografica"))

    print(f"{len(raw)} extrações → {OUT_DIR/'protest_events_raw.csv'}")
    print(f"{len(df)} eventos ({len(eligible)} elegíveis) → "
          f"{OUT_DIR/'protest_events.csv'} e .xlsx")


if __name__ == "__main__":
    events = assign_canonical(normalize(load_events()))
    export(events, collapse(events))
