"""check_bib.py — Confere referencias.bib contra referencias-abnt.md.

Verifica (1) que o .bib parseia, (2) que toda obra da lista ABNT tem entrada
correspondente no .bib, e (3) lista as entradas ainda marcadas para verificação
bibliográfica.

Uso: python check_bib.py     (código de saída 1 se houver sobrenome sem cobertura)
"""

import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
BIB = BASE / "referencias.bib"
ABNT = BASE / "referencias-abnt.md"

ENTRY_RE = re.compile(r"^@(\w+)\{([^,]+),", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*(\w+)\s*=\s*", re.MULTILINE)


def deaccent(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def parse_bib(raw: str):
    entries = {}
    positions = [(m.start(), m.group(1), m.group(2)) for m in ENTRY_RE.finditer(raw)]
    for i, (start, etype, key) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(raw)
        entries[key] = {"type": etype, "body": raw[start:end]}
    return entries


def main() -> int:
    raw = BIB.read_text(encoding="utf-8")

    # Balanço de chaves: detecta entrada truncada.
    if raw.count("{") != raw.count("}"):
        print(f"ERRO: chaves desbalanceadas no .bib "
              f"({raw.count('{')} '{{' vs {raw.count('}')} '}}')")
        return 1

    entries = parse_bib(raw)
    dup = [k for k in entries if list(entries).count(k) > 1]
    if dup:
        print(f"ERRO: chaves duplicadas: {sorted(set(dup))}")
        return 1

    obrigatorios = {"title", "year"}
    incompletas = []
    for key, e in entries.items():
        campos = set(FIELD_RE.findall(e["body"]))
        faltam = obrigatorios - campos
        if faltam:
            incompletas.append(f"{key}: sem {sorted(faltam)}")

    a_verificar = [k for k, e in entries.items() if "VERIFICAR" in e["body"]]

    # Cobertura: todo SOBRENOME em CAIXA-ALTA iniciando linha na lista ABNT
    # deve aparecer em algum campo author/editor do .bib.
    abnt = ABNT.read_text(encoding="utf-8")
    sobrenomes = set()
    for line in abnt.splitlines():
        m = re.match(r"^([A-ZÀ-Ý][A-ZÀ-Ýa-zà-ý'\-]*(?: [A-ZÀ-Ý]{2,})?),", line.strip())
        if m:
            sobrenomes.add(deaccent(m.group(1)).split()[0])
    bib_flat = deaccent(raw)
    sem_cobertura = sorted(s for s in sobrenomes if s not in bib_flat)

    print(f"{len(entries)} entradas no .bib "
          f"({len(sobrenomes)} sobrenomes distintos na lista ABNT)")
    if incompletas:
        print(f"\nEntradas sem campo obrigatório ({len(incompletas)}):")
        for i in incompletas:
            print(f"  - {i}")
    if a_verificar:
        print(f"\nEntradas marcadas para verificação bibliográfica ({len(a_verificar)}):")
        for k in sorted(a_verificar):
            print(f"  - {k}")
    if sem_cobertura:
        print(f"\nSobrenomes da lista ABNT SEM entrada no .bib ({len(sem_cobertura)}):")
        for s in sem_cobertura:
            print(f"  - {s}")
        return 1

    print("\nOK: toda obra da lista ABNT tem entrada correspondente no .bib.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
