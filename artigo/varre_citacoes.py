"""varre_citacoes.py — Nenhuma obra citada sem entrada no .bib.

Varre process-tracing/ e codebook/ atrás de citações no formato autor-data
— "SOBRENOME (2019)", "Sobrenome e Outro (2001)", "(SOBRENOME, 2019)" — e
confere se o sobrenome aparece em algum campo author/editor de
artigo/referencias.bib.

Foi esta varredura que revelou, em 2026-08-23, doze obras citadas nos codebooks
e no protocolo de process tracing sem entrada bibliográfica — inclusive José de
Souza (1986), âncora das quatro dimensões do T-1 conjuntural.

Uso: python artigo/varre_citacoes.py [--estrito]
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
BIB = BASE / "referencias.bib"
ALVOS = ["process-tracing", "codebook", "docs"]
EXTENSOES = {".md", ".yaml", ".yml"}

# Sobrenome seguido de ano entre parênteses. Captura "Tarrow (2009)",
# "MCADAM, TARROW e TILLY (2001)" e "(HOLDO, 2019)".
CITACAO = re.compile(r"\b([A-ZÀ-Ý][a-zà-ýA-ZÀ-Ý'\-]{2,})\s*[,(]\s*(\d{4})\)?")

# Palavras que casam o padrão sem serem autoria.
RUIDO = {
    "figura", "quadro", "tabela", "secao", "seção", "fase", "ciclo", "protocolo",
    "codebook", "anexo", "nota", "desde", "entre", "junho", "outubro", "abril",
    "dezembro", "setembro", "novembro", "janeiro", "marco", "março", "maio",
    "agosto", "julho", "fevereiro", "diretas", "collor", "dilma", "brasil",
    "camara", "câmara", "senado", "constituicao", "constituição", "resolucao",
    "resolução", "emenda", "colegio", "colégio", "impeachment", "lei", "artigo",
    "decreto", "diario", "diário", "acervo", "folha", "sessao", "sessão", "pec",
    "verificado", "registrada", "revisada", "criado", "atualizado", "incorporada",
    "incorporadas", "aprovada", "rejeitada", "eleicao", "eleição", "votacao",
    "votação", "magnitude", "abertura", "reversao", "reversão", "predicao",
    "predição", "predicoes", "hipotese", "hipótese", "evidencia", "evidência",
    # topônimos e nomes próprios de eventos/instituições que casam o padrão
    "salvador", "candelaria", "candelária", "caras-pintadas", "cansei", "nepac",
    "constituinte", "eleitoral", "pnadc", "pnad", "resolvido", "ufjf", "unicamp",
    "anhangabau", "anhangabaú", "se", "sé",
}


def deaccent(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def main(estrito: bool) -> int:
    bib = deaccent(BIB.read_text(encoding="utf-8"))
    achados: dict[str, set[str]] = {}

    for alvo in ALVOS:
        for caminho in (RAIZ / alvo).rglob("*"):
            if caminho.suffix.lower() not in EXTENSOES or not caminho.is_file():
                continue
            texto = caminho.read_text(encoding="utf-8", errors="ignore")
            for sobrenome, ano in CITACAO.findall(texto):
                chave = deaccent(sobrenome)
                if chave in RUIDO or len(chave) < 3 or not (1900 <= int(ano) <= 2030):
                    continue
                if chave not in bib:
                    achados.setdefault(f"{sobrenome} ({ano})", set()).add(
                        str(caminho.relative_to(RAIZ)))

    print(f"Varredura em {', '.join(ALVOS)} contra {BIB.name}")
    if not achados:
        print("\nOK: toda citação autor-data tem sobrenome correspondente no .bib.")
        return 0

    print(f"\nCitações SEM entrada no .bib ({len(achados)}):")
    for cit in sorted(achados):
        print(f"  - {cit}")
        for arq in sorted(achados[cit]):
            print(f"      {arq}")
    print("\nNem toda ocorrência é autoria; confira antes de agir. "
          "Se for ruído recorrente, acrescente o termo ao conjunto RUIDO.")
    return 1 if estrito else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--estrito", action="store_true")
    sys.exit(main(ap.parse_args().estrito))
