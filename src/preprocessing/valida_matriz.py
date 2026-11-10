#!/usr/bin/env python3
"""valida_matriz.py — Confere teoria/matriz.yaml e gera a tabela de teoria/README.md.

Checa que cada conceito usa só chaves de docs/artigo/referencias.bib, só
variáveis de bancos/03_aep_br/codebook/codebook_aep_br.yaml e só dimensões e
status declarados; que conceitos `a_criar` trazem a candidata e conceitos
`derivado` trazem a medida; e que o campo `conceito` das variáveis do codebook
aponta para um conceito existente. Depois reescreve a tabela entre os marcadores
MATRIZ:INICIO e MATRIZ:FIM do README e lista as variáveis do codebook que nenhum
conceito usa.

Uso:
  python src/preprocessing/valida_matriz.py           # valida e atualiza o README
  python src/preprocessing/valida_matriz.py --check   # só valida; falha se o README estiver defasado
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

MATRIZ = paths.RAIZ / "teoria" / "matriz.yaml"
README = paths.RAIZ / "teoria" / "README.md"
INICIO = "<!-- MATRIZ:INICIO — gerado por src/preprocessing/valida_matriz.py, não editar à mão -->"
FIM = "<!-- MATRIZ:FIM -->"
NIVEIS = {"evento", "serie", "externo"}
OBRIGATORIOS = ("id", "conceito", "dimensao", "definicao", "referencias", "nivel", "status", "variaveis")


def erros_da_matriz(m: dict, chaves_bib: set, variaveis: set) -> list[str]:
    erros, ids = [], set()
    for c in m["conceitos"]:
        cid = c.get("id", "?")
        erros += [f"{cid}: falta o campo {k}" for k in OBRIGATORIOS if k not in c]
        if cid in ids:
            erros.append(f"{cid}: id repetido")
        ids.add(cid)
        if c.get("dimensao") not in m["dimensoes"]:
            erros.append(f"{cid}: dimensão desconhecida {c.get('dimensao')!r}")
        if c.get("status") not in m["status"]:
            erros.append(f"{cid}: status desconhecido {c.get('status')!r}")
        if c.get("nivel") not in NIVEIS:
            erros.append(f"{cid}: nível desconhecido {c.get('nivel')!r}")
        if not c.get("referencias"):
            erros.append(f"{cid}: sem referência")
        erros += [f"{cid}: chave {r!r} ausente do .bib" for r in c.get("referencias", []) if r not in chaves_bib]
        erros += [f"{cid}: variável {v!r} ausente do codebook" for v in c.get("variaveis", []) if v not in variaveis]
        if c.get("status") == "a_criar" and not all(c.get("candidata", {}).get(k) for k in ("nome", "conteudo", "risco")):
            erros.append(f"{cid}: status a_criar exige candidata com nome, conteudo e risco")
        if c.get("status") == "derivado" and not c.get("medida_derivada"):
            erros.append(f"{cid}: status derivado exige medida_derivada")
    return erros


def tabela(m: dict) -> str:
    linhas = ["| Dimensão | Conceito | Nível | Status | Variáveis ou candidata | Referências |",
              "|---|---|---|---|---|---|"]
    for c in m["conceitos"]:
        vs = ", ".join(f"`{v}`" for v in c["variaveis"]) or "—"
        if c["status"] == "a_criar":
            vs = f"proposta: `{c['candidata']['nome']}`" + (f" (hoje: {vs})" if c["variaveis"] else "")
        linhas.append(f"| {m['dimensoes'][c['dimensao']]} | {c['conceito']} | {c['nivel']} | "
                      f"{c['status']} | {vs} | {', '.join(c['referencias'])} |")
    return "\n".join(linhas)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="não reescreve o README; falha se estiver defasado")
    args = ap.parse_args()

    m = yaml.safe_load(MATRIZ.read_text(encoding="utf-8"))
    chaves_bib = set(re.findall(r"^@\w+\{([^,\s]+),", paths.BIB.read_text(encoding="utf-8"), re.M))
    codebook = yaml.safe_load(paths.AEP_CODEBOOK.read_text(encoding="utf-8"))
    variaveis = {v["nome"] for v in codebook["variaveis"]}

    erros = erros_da_matriz(m, chaves_bib, variaveis)
    ids = {c["id"] for c in m["conceitos"]}
    erros += [f"codebook: {v['nome']} aponta para o conceito inexistente {v['conceito']!r}"
              for v in codebook["variaveis"] if v.get("conceito") and v["conceito"] not in ids]
    if erros:
        print("Matriz com problemas:")
        print("\n".join(f"  - {e}" for e in erros))
        return 1

    texto = README.read_text(encoding="utf-8")
    assert INICIO in texto and FIM in texto, f"marcadores ausentes em {README}"
    novo = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIM),
                  lambda _: f"{INICIO}\n{tabela(m)}\n{FIM}", texto, flags=re.S)
    if args.check and novo != texto:
        print("teoria/README.md defasado em relação à matriz. Rode sem --check.")
        return 1
    if novo != texto:
        README.write_text(novo, encoding="utf-8")

    usadas = ({v for c in m["conceitos"] for v in c["variaveis"]}
              | {v["nome"] for v in codebook["variaveis"] if v.get("conceito")})
    contagem = {s: sum(c["status"] == s for c in m["conceitos"]) for s in m["status"]}
    print(f"OK: {len(m['conceitos'])} conceitos; " + ", ".join(f"{s} {n}" for s, n in contagem.items()))
    sem_conceito = sorted(variaveis - usadas)
    print(f"Variáveis do codebook sem conceito associado ({len(sem_conceito)}): {', '.join(sem_conceito)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
