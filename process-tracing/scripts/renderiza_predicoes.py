"""renderiza_predicoes.py — Escreve as predições nos dossiês a partir do CSV.

Fonte de verdade: process-tracing/dados/predicoes.csv.
Derivado: a seção "Predições registradas" de cada ciclos/c*/dossie.md, entre os
marcadores PREDICOES:INICIO e PREDICOES:FIM.

Mesmo padrão que artigo/referencias.bib -> referencias-abnt.md: edite o CSV,
nunca a tabela renderizada — ela é sobrescrita a cada execução.

Uso:
  python renderiza_predicoes.py            # renderiza
  python renderiza_predicoes.py --check    # só confere; sai 1 se dessincronizado
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "dados" / "predicoes.csv"
INICIO = "<!-- PREDICOES:INICIO — gerado por scripts/renderiza_predicoes.py, não editar à mão -->"
FIM = "<!-- PREDICOES:FIM -->"

DOSSIES = {
    "c1": "c1-diretas-ja", "c2": "c2-fora-collor",
    "c3": "c3-junho-2013", "c4": "c4-impeachment-dilma",
}

ROTULO = {
    "ancora": "âncora — a hipótese foi construída a partir deste ciclo; **não é teste**",
    "fora_de_amostra": "fora de amostra — **teste genuíno**",
    "nao_pertinente": "não pertinente ao desenho",
}
ORDEM = ["fora_de_amostra", "ancora", "nao_pertinente"]


def bloco(df_ciclo: pd.DataFrame) -> str:
    n_fora = int((df_ciclo.estatuto_probatorio == "fora_de_amostra").sum())
    n_anc = int((df_ciclo.estatuto_probatorio == "ancora").sum())
    n_np = int((df_ciclo.estatuto_probatorio == "nao_pertinente").sum())
    data = df_ciclo.data_registro.max()

    L = [INICIO, ""]
    L.append(f"**Registradas em {data}**, antes de qualquer varredura (PROTOCOLO §5). "
             f"{len(df_ciclo)} predições: {n_fora} fora de amostra, {n_anc} de âncora, "
             f"{n_np} não pertinentes.")
    L.append("")
    L.append("O *estatuto probatório* distingue o que pode ser testado do que não pode. "
             "Onde a evidência-âncora da hipótese em `docs/quadro-hipoteses.md` vem deste "
             "ciclo, a hipótese foi formulada olhando para ele: a predição é reformulação, "
             "não previsão, e nenhuma evidência aqui pode refutá-la. Só as predições **fora "
             "de amostra** constituem teste.")
    L.append("")
    L.append("Fonte de verdade: `dados/predicoes.csv`. Esta seção é gerada — não editar aqui.")
    L.append("")

    for est in ORDEM:
        sub = df_ciclo[df_ciclo.estatuto_probatorio == est]
        if sub.empty:
            continue
        L.append(f"### {ROTULO[est].split(' — ')[0].capitalize()} ({len(sub)})")
        L.append("")
        if est == "fora_de_amostra":
            L.append("*Estas são as predições que podem falhar.*")
        elif est == "ancora":
            L.append("*Registradas por completude e para o trabalho documental; "
                     "não testam a hipótese.*")
        L.append("")
        for _, r in sub.sort_values("hipotese").iterrows():
            L.append(f"**{r.hipotese}**")
            L.append("")
            L.append(f"- *Predição.* {r.predicao}")
            L.append(f"- *O que a refutaria.* {r.o_que_refutaria}")
            if str(r.teste_van_evera_previsto).strip() and r.teste_van_evera_previsto != "—":
                L.append(f"- *Teste previsto:* {str(r.teste_van_evera_previsto).replace('_', ' ')} "
                         f"· *Indicador:* {r.indicador_operacional} "
                         f"· *Fonte prevista:* {r.fonte_prevista}")
            L.append("")
    L.append(FIM)
    return "\n".join(L)


def aplica(texto: str, novo: str) -> str:
    if INICIO in texto and FIM in texto:
        antes = texto.split(INICIO)[0]
        depois = texto.split(FIM, 1)[1]
        return antes + novo + depois
    # primeira execução: substitui a seção placeholder até o fim do arquivo
    marca = "## Predições registradas"
    if marca not in texto:
        raise SystemExit(f"seção '{marca}' não encontrada no dossiê")
    return texto.split(marca)[0] + marca + "\n\n" + novo + "\n"


def main(check: bool) -> None:
    df = pd.read_csv(CSV, dtype=str)
    divergentes = []
    for ciclo, pasta in DOSSIES.items():
        caminho = BASE / "ciclos" / pasta / "dossie.md"
        atual = caminho.read_text(encoding="utf-8")
        sub = df[df.ciclo == ciclo]
        if sub.empty:
            print(f"[aviso] nenhuma predição para {ciclo}")
            continue
        novo = aplica(atual, bloco(sub))
        if novo == atual:
            print(f"  {ciclo}: em dia ({len(sub)} predições)")
            continue
        if check:
            divergentes.append(pasta)
            print(f"  {ciclo}: DESSINCRONIZADO")
            continue
        caminho.write_text(novo, encoding="utf-8")
        print(f"  {ciclo}: {len(sub)} predições renderizadas → {caminho.name}")

    if check and divergentes:
        print(f"\n{len(divergentes)} dossiê(s) fora de sincronia com o CSV. "
              "Rode sem --check para atualizar.")
        sys.exit(1)
    if check:
        print("\nTodos os dossiês em sincronia com o CSV.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="não escreve; sai com código 1 se houver divergência")
    main(ap.parse_args().check)
