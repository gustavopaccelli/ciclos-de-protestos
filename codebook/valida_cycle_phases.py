"""valida_cycle_phases.py — Confere data/cycle_phases.csv contra o codebook.

Checa:
  1. Vocabulários: todo valor categórico consta de cycle_phases_codebook.yaml.
  2. Faixa: variáveis ordinais em 0-3, ou NA (que é distinto de 0).
  3. Regra de ortogonalidade: traducao_direcao é NA se e somente se
     traducao_institucional = 0. Mesma regra para valência e controle.
  4. Periodização: 6 fases por ciclo, sem lacuna nem sobreposição.
  5. Trilha de auditoria: toda mudança de escore em relação à versão em git
     precisa de linha correspondente em codebook/historico-codificacao.csv.

Uso: python codebook/valida_cycle_phases.py [--estrito]
"""

import argparse
import io
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
CSV = RAIZ / "data" / "cycle_phases.csv"
CODEBOOK = BASE / "cycle_phases_codebook.yaml"
HISTORICO = BASE / "historico-codificacao.csv"

erros: list[str] = []
avisos: list[str] = []

ORDINAIS_PREFIXO = ("op_", "od_")
CATEGORICAS = ["traducao_direcao", "traducao_valencia", "traducao_controle_gatilho"]


def secao(t: str) -> None:
    print(f"\n{t}\n{'-' * len(t)}")


def carrega():
    # keep_default_na=False para que a string "NA" não vire NaN — a distinção
    # entre NA (não se aplica) e 0 (medido e ausente) é regra do codebook.
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False)
    cb = yaml.safe_load(CODEBOOK.read_text(encoding="utf-8"))
    return df, cb


def checa_vocabulario(df, cb):
    secao("1. Vocabulário controlado")
    bloco = cb["blocos"]["traducao_institucional"]
    for campo in CATEGORICAS:
        if campo not in df.columns:
            erros.append(f"coluna ausente: {campo}")
            continue
        vocab = set(bloco[campo]["valores"])
        fora = set(df[campo]) - vocab
        if fora:
            erros.append(f"{campo}: valores fora do codebook -> {sorted(fora)}")
        else:
            print(f"  {campo}: {df[campo].nunique()} valores distintos, todos no codebook")


def checa_faixa(df):
    secao("2. Faixa das ordinais")
    cols = [c for c in df.columns if c.startswith(ORDINAIS_PREFIXO)] + ["traducao_institucional"]
    for c in cols:
        vals = set(df[c])
        ruins = {v for v in vals if v != "NA" and v not in {"0", "1", "2", "3"}}
        if ruins:
            erros.append(f"{c}: valores fora de 0-3/NA -> {sorted(ruins)}")
    print(f"  {len(cols)} variáveis ordinais conferidas")
    na = sum((df[c] == "NA").sum() for c in cols)
    print(f"  {na} células NA (distintas de 0, conforme codebook)")


def checa_ortogonalidade(df):
    secao("3. Ortogonalidade magnitude x direção")
    mag_zero = df.traducao_institucional == "0"
    for campo in CATEGORICAS:
        deve_na = set(df.loc[mag_zero, "phase_id"])
        eh_na = set(df.loc[df[campo] == "NA", "phase_id"])
        if deve_na != eh_na:
            faltam = sorted(deve_na - eh_na)
            sobram = sorted(eh_na - deve_na)
            if faltam:
                erros.append(f"{campo}: magnitude 0 mas valor preenchido em {faltam}")
            if sobram:
                erros.append(f"{campo}: NA com magnitude > 0 em {sobram}")
    print(f"  {int(mag_zero.sum())} fases com magnitude 0 -> direção/valência/controle = NA")
    print(f"  {int((~mag_zero).sum())} fases com magnitude > 0 -> todas classificadas")

    des = df[df.phase == "desfecho"]
    n = des.traducao_direcao.nunique()
    print(f"\n  Direções nos desfechos: {n} distintas em {len(des)} ciclos")
    for _, r in des.iterrows():
        print(f"    {r.cycle:<20} {r.traducao_direcao}")
    if n < len(des):
        avisos.append("dois ou mais ciclos com a mesma direção no desfecho — "
                      "a tipologia pode não estar discriminando")


def checa_periodizacao(df):
    secao("4. Periodização")
    d = df.copy()
    d["s"] = pd.to_datetime(d.date_start)
    d["e"] = pd.to_datetime(d.date_end)
    for c, g in d.groupby("cycle"):
        g = g.sort_values("s")
        if len(g) != 6:
            avisos.append(f"{c}: {len(g)} fases (esperado 6)")
        for (_, a), (_, b) in zip(g.iterrows(), g.iloc[1:].iterrows()):
            gap = (b.s - a.e).days
            if gap != 1:
                erros.append(f"{c}: {a.phase_id} -> {b.phase_id} com intervalo de {gap} dias")
    print(f"  {d.cycle.nunique()} ciclos, {len(d)} fases, sem lacuna nem sobreposição")


def checa_trilha(df):
    secao("5. Trilha de auditoria")
    if not HISTORICO.exists():
        erros.append("codebook/historico-codificacao.csv ausente")
        return
    hist = pd.read_csv(HISTORICO, dtype=str)
    print(f"  {len(hist)} registros em historico-codificacao.csv")

    try:
        git = subprocess.run(["git", "show", "HEAD:data/cycle_phases.csv"],
                             cwd=RAIZ, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        avisos.append("não foi possível ler a versão em git — trilha não comparada")
        return
    antes = pd.read_csv(io.StringIO(git.stdout), dtype=str, keep_default_na=False)

    cols = [c for c in antes.columns
            if c.startswith(ORDINAIS_PREFIXO) or c == "traducao_institucional"]
    m = antes.merge(df, on="phase_id", suffixes=("_antes", "_agora"))
    mudancas = []
    for c in cols:
        if f"{c}_antes" not in m or f"{c}_agora" not in m:
            continue
        dif = m[m[f"{c}_antes"] != m[f"{c}_agora"]]
        for _, r in dif.iterrows():
            mudancas.append((r.phase_id, c, r[f"{c}_antes"], r[f"{c}_agora"]))

    if not mudancas:
        print("  nenhum escore alterado em relação a HEAD")
        return
    registradas = set()
    for _, r in hist.iterrows():
        for pid in str(r.get("phase_id", "")).split(";"):
            registradas.add((pid.strip(), str(r.get("variavel", "")).strip()))
    for pid, var, a, b in mudancas:
        if (pid, var) not in registradas and ("TODAS", var) not in registradas:
            erros.append(f"{pid}/{var}: {a} -> {b} sem registro em historico-codificacao.csv")
        else:
            print(f"  {pid}/{var}: {a} -> {b} (registrado)")


def main(estrito: bool) -> None:
    df, cb = carrega()
    print(f"{len(df)} fases · {len(df.columns)} variáveis · codebook v{cb.get('versao', '?')}")
    checa_vocabulario(df, cb)
    checa_faixa(df)
    checa_ortogonalidade(df)
    checa_periodizacao(df)
    checa_trilha(df)

    secao("Resultado")
    for a in avisos:
        print(f"  [aviso] {a}")
    for e in erros:
        print(f"  [ERRO]  {e}")
    if not erros and not avisos:
        print("  Nenhum problema encontrado.")
    print(f"\n  {len(erros)} erros, {len(avisos)} avisos")
    if estrito and erros:
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--estrito", action="store_true")
    main(ap.parse_args().estrito)
