"""lista_verificacao.py — Checklist das entradas com metadados a confirmar.

Gera literature/verificacao-bibliografica.md a partir de referencias.bib,
listando toda entrada marcada com VERIFICAR: o que a nota pede para conferir e
quais campos estão vazios.

Arquivo DERIVADO — mesmo padrão de referencias.bib -> referencias-abnt.md.
Edite o .bib e regenere; não edite o .md à mão.

Uso: python artigo/lista_verificacao.py [--check]
"""

import argparse
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
BIB = BASE / "referencias.bib"
SAIDA = BASE.parent / "literature" / "verificacao-bibliografica.md"

ENTRY = re.compile(r"^@(\w+)\{([^,]+),", re.MULTILINE)
# Campos que não se aplicam a cada tipo — evita cobrar volume de livro.
NAO_SE_APLICA = {
    "book": {"volume", "number", "pages", "journal", "doi"},
    "misc": {"volume", "number", "journal", "doi", "publisher", "address"},
    "incollection": {"volume", "number", "journal", "doi"},
    "article": {"publisher", "address"},
}
CONFERIR = ["journal", "booktitle", "volume", "number", "pages", "doi", "publisher", "address"]


def campo(corpo: str, nome: str) -> str:
    m = re.search(rf"^\s*{nome}\s*=\s*\{{(.*?)\}},?\s*$", corpo, re.MULTILINE | re.DOTALL)
    return " ".join(m.group(1).split()) if m else ""


def coleta() -> list[dict]:
    raw = BIB.read_text(encoding="utf-8")
    pos = [(m.start(), m.group(1), m.group(2)) for m in ENTRY.finditer(raw)]
    itens = []
    for i, (s, tipo, chave) in enumerate(pos):
        corpo = raw[s: pos[i + 1][0] if i + 1 < len(pos) else len(raw)]
        if "VERIFICAR" not in corpo:
            continue
        nota = campo(corpo, "note")
        m = re.search(r"VERIFICAR:?\s*(.*?)(?:\.\s|$)", nota)
        vazios = [c for c in CONFERIR
                  if not campo(corpo, c) and c not in NAO_SE_APLICA.get(tipo, set())]
        itens.append({
            "chave": chave, "tipo": tipo,
            "autor": campo(corpo, "author") or campo(corpo, "editor") or "—",
            "titulo": campo(corpo, "title"), "ano": campo(corpo, "year") or "s.d.",
            "pede": (m.group(1).strip() if m else ""), "vazios": vazios,
        })
    return sorted(itens, key=lambda x: x["chave"])


def render(itens: list[dict]) -> str:
    L = ["# Verificação bibliográfica pendente", "",
         "Entradas de `artigo/referencias.bib` marcadas com `VERIFICAR`: os metadados estão",
         "incompletos ou não foram conferidos em fonte primária. Enquanto assim estiverem, a",
         "citação é utilizável no texto, mas a referência **não deve ir para publicação**.", "",
         "> **Arquivo derivado.** Gerado por `artigo/lista_verificacao.py` a partir do `.bib`.",
         "> Corrija o `.bib` e regenere; não edite este arquivo à mão. Ao completar uma",
         "> entrada, remova a nota `VERIFICAR` do `.bib` e ela sai desta lista sozinha.", "",
         f"**{len(itens)} entradas pendentes.**", "",
         "Nenhum campo será preenchido por inferência: um metadado plausível porém não",
         "conferido é pior que um campo vazio, porque parece verificado.", "", "---", ""]
    for it in itens:
        titulo = it["titulo"].replace("{", "").replace("}", "")
        L.append(f"### `{it['chave']}`")
        L.append("")
        L.append(f"{it['autor']} — *{titulo}* ({it['ano']}, {it['tipo']})")
        L.append("")
        if it["pede"]:
            L.append(f"- **A nota pede:** {it['pede']}")
        if it["vazios"]:
            L.append(f"- **Campos vazios:** {', '.join(f'`{c}`' for c in it['vazios'])}")
        if not it["pede"] and not it["vazios"]:
            L.append("- Marcada para verificação sem detalhamento — conferir a entrada inteira.")
        L.append("")
    return "\n".join(L)


def main(check: bool) -> int:
    itens = coleta()
    novo = render(itens)
    if check:
        atual = SAIDA.read_text(encoding="utf-8") if SAIDA.exists() else ""
        if atual != novo:
            print("Checklist dessincronizado do .bib. Rode sem --check.")
            return 1
        print(f"OK: checklist em dia ({len(itens)} entradas pendentes).")
        return 0
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(novo, encoding="utf-8")
    print(f"{len(itens)} entradas pendentes → {SAIDA.relative_to(BASE.parent)}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    sys.exit(main(ap.parse_args().check))
