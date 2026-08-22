"""valida_registro.py — Integridade e cobertura do levantamento por process tracing.

Roda sem rede. Checa o que um parecerista checaria:

  1. Chaves estrangeiras: fase_vinculada existe em data/cycle_phases.csv e a data
     do evento cai dentro da fase; hipotese_vinculada existe no quadro de hipóteses.
  2. Procedência: nada marcado como verificado_* sem fonte_url e data_consulta.
  3. Vocabulário: todo valor categórico consta do codebook.
  4. Cobertura: matriz ciclo x tempo, e células vazias do Quadro 8 ampliado.
  5. Desconfirmação: contagem por hipótese. Zero desconfirmação em 14 hipóteses
     é sinal de viés de busca, não de força do argumento (PROTOCOLO §5).
  6. Cadeia entre ciclos: todo marco com ciclo_seguinte_afetado deve ter
     evidencia_id, senão H3.5 fica sem lastro empírico.

Uso: python process-tracing/scripts/valida_registro.py [--estrito]
     --estrito faz o script sair com código 1 se houver qualquer erro.
"""

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

BASE = Path(__file__).resolve().parent.parent
RAIZ = BASE.parent
DADOS = BASE / "dados"

erros: list[str] = []
avisos: list[str] = []


def secao(titulo: str) -> None:
    print(f"\n{titulo}\n{'-' * len(titulo)}")


def carregar():
    cb = yaml.safe_load((BASE / "codebook-evidencia.yaml").read_text(encoding="utf-8"))
    ev = pd.read_csv(DADOS / "registro_evidencias.csv", dtype=str)
    mi = pd.read_csv(DADOS / "marcos_institucionais.csv", dtype=str)
    q8 = pd.read_csv(DADOS / "quadro8_ampliado.csv", dtype=str)
    fases = pd.read_csv(RAIZ / "data" / "cycle_phases.csv", dtype=str)
    hip = set(re.findall(r"H\d\.\d",
                         (RAIZ / "docs" / "quadro-hipoteses.md").read_text(encoding="utf-8")))
    return cb, ev, mi, q8, fases, hip


def checa_fks(ev, fases, hip):
    secao("1. Chaves estrangeiras")
    validas = set(fases.phase_id)
    faixa = fases.set_index("phase_id")[["date_start", "date_end"]].to_dict("index")

    com_fase = ev[ev.fase_vinculada.notna()]
    for _, r in com_fase.iterrows():
        if r.fase_vinculada not in validas:
            erros.append(f"{r.evidencia_id}: fase '{r.fase_vinculada}' não existe")
            continue
        f = faixa[r.fase_vinculada]
        if pd.notna(r.data_evento) and not (f["date_start"] <= r.data_evento <= f["date_end"]):
            erros.append(
                f"{r.evidencia_id}: data {r.data_evento} fora de {r.fase_vinculada} "
                f"({f['date_start']} a {f['date_end']})"
            )
    print(f"  {len(com_fase)} evidências com fase vinculada; "
          f"{len(ev) - len(com_fase)} sem (aceitável em T-1e e T+1 longo)")

    ruins = set(ev.hipotese_vinculada.dropna()) - hip
    if ruins:
        erros.append(f"hipóteses inexistentes no quadro: {sorted(ruins)}")
    print(f"  {len(hip)} hipóteses no quadro; {ev.hipotese_vinculada.nunique()} referenciadas")


def checa_procedencia(ev):
    secao("2. Procedência")
    verif = ev[ev.status_verificacao.fillna("").str.startswith(("verificado", "corroborado"))]
    for _, r in verif.iterrows():
        if pd.isna(r.fonte_url) or not str(r.fonte_url).strip():
            erros.append(f"{r.evidencia_id}: marcado '{r.status_verificacao}' sem fonte_url")
        if pd.isna(r.data_consulta):
            erros.append(f"{r.evidencia_id}: marcado '{r.status_verificacao}' sem data_consulta")
    nivel = pd.to_numeric(ev.fonte_nivel, errors="coerce")
    t1 = ev[(ev.tempo == "T+1") & (nivel > 2)]
    for _, r in t1.iterrows():
        erros.append(f"{r.evidencia_id}: T+1 com fonte nível {r.fonte_nivel} "
                     "(regra de admissibilidade exige 1 ou 2)")
    print(f"  {len(verif)} evidências verificadas/corroboradas")
    print(f"  {(ev.status_verificacao == 'pendente').sum()} pendentes | "
          f"{(ev.status_verificacao == 'divergencia_nao_resolvida').sum()} com divergência aberta")


def checa_vocabulario(cb, ev):
    secao("3. Vocabulário controlado")
    campos = {
        "tempo": set(cb["tempos"]),
        "dimensao_conjuntura": set(cb["dimensoes_conjuntura"]),
        "mecanismo": set(cb["mecanismos"]),
        "teste_van_evera": set(cb["testes_van_evera"]),
        "relacao_com_hipotese": set(cb["relacao_com_hipotese"]),
        "status_verificacao": set(cb["status_verificacao"]),
        "ciclo": set(cb["ciclos"]),
    }
    for campo, vocab in campos.items():
        fora = set(ev[campo].dropna()) - vocab
        if fora:
            erros.append(f"{campo}: valores fora do codebook → {sorted(fora)}")
    print(f"  {len(campos)} campos conferidos contra o codebook")


def checa_cobertura(ev, q8):
    secao("4. Cobertura")
    print(pd.crosstab(ev.ciclo, ev.tempo).to_string())
    vazias = q8[q8.formulacao_tese_2024.isna() | (q8.formulacao_tese_2024.fillna("") == "")]
    print(f"\n  Quadro 8 ampliado: {len(q8)} células, {len(vazias)} sem formulação na tese")
    if len(vazias):
        print(f"  ciclos com células vazias: {sorted(vazias.ciclo.unique())} "
              "(esperado: c1, que a tese não trata como estudo de caso)")
    sem_ancora = q8[q8.evidencia_ids.fillna("") == ""]
    print(f"  {len(sem_ancora)} células ainda sem evidencia_id — o mapa do que falta")


def checa_desconfirmacao(ev, hip):
    secao("5. Desconfirmação por hipótese")
    d = ev[ev.relacao_com_hipotese == "desconfirma"].groupby("hipotese_vinculada").size()
    c = ev[ev.relacao_com_hipotese == "confirma"].groupby("hipotese_vinculada").size()
    tab = pd.DataFrame({"confirma": c, "desconfirma": d}).fillna(0).astype(int)
    print(tab.to_string() if len(tab) else "  (nenhuma evidência vinculada ainda)")
    if len(ev) >= 30 and tab.get("desconfirma", pd.Series(dtype=int)).sum() == 0:
        avisos.append("nenhuma evidência desconfirmatória em 30+ registros — "
                      "revisar a estratégia de busca (PROTOCOLO §5)")
    sem_ev = sorted(hip - set(ev.hipotese_vinculada.dropna()))
    print(f"\n  {len(sem_ev)} hipóteses sem nenhuma evidência: {', '.join(sem_ev) or '—'}")


def checa_cadeia(mi):
    secao("6. Cadeia entre ciclos (lastro de H3.5)")
    elos = mi[mi.ciclo_seguinte_afetado.notna()]
    if elos.empty:
        avisos.append("nenhum marco encadeia ciclos — H3.5 sem lastro empírico")
    for _, r in elos.iterrows():
        if pd.isna(r.evidencia_id):
            erros.append(f"{r.marco_id}: encadeia para {r.ciclo_seguinte_afetado} "
                         "sem evidencia_id")
        print(f"  {r.marco_id} ({r.data}) {r.ciclo} → {r.ciclo_seguinte_afetado} "
              f"[{r.status_verificacao}]")


def main(estrito: bool) -> None:
    cb, ev, mi, q8, fases, hip = carregar()
    print(f"Registro: {len(ev)} evidências | {len(mi)} marcos | {len(q8)} células do Quadro 8")
    checa_fks(ev, fases, hip)
    checa_procedencia(ev)
    checa_vocabulario(cb, ev)
    checa_cobertura(ev, q8)
    checa_desconfirmacao(ev, hip)
    checa_cadeia(mi)

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
    ap.add_argument("--estrito", action="store_true",
                    help="sai com código 1 se houver erro (uso em CI)")
    main(ap.parse_args().estrito)
