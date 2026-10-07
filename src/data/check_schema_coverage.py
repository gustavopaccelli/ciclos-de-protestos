"""check_schema_coverage.py — Confere o coder contra o codebook AEP-BR.

Verifica que:
- toda variável de bancos/03_aep_br/codebook/codebook_aep_br.yaml é pedida ao
  modelo (EVENT_PROPERTIES) ou atribuída pelo pipeline (CAMPOS_PIPELINE), e
  que o coder não gera campo fora do codebook;
- cada enum do schema é exatamente o vocabulário do codebook;
- o system prompt carrega a regra do MAIOR público e as decisões da versão.

Este teste existe porque a divergência entre coder e codebook era invisível:
em 2026-07 o coder implementava ~16 dos ~40 campos declarados.

Uso: python src/data/check_schema_coverage.py   (código de saída 1 se houver divergência)
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402


def load_coder():
    spec = importlib.util.spec_from_file_location(
        "coder", paths.RAIZ / "src" / "preprocessing" / "coder.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    coder = load_coder()
    cb = coder.cb
    problemas = []

    declarados = set(cb.nomes())
    implementados = set(coder.EVENT_PROPERTIES) | coder.CAMPOS_PIPELINE
    if declarados - implementados:
        problemas.append(f"variáveis do codebook NÃO implementadas: {sorted(declarados - implementados)}")
    if implementados - declarados:
        problemas.append(f"campos fora do codebook: {sorted(implementados - declarados)}")
    pedidos_e_pipeline = set(coder.EVENT_PROPERTIES) & coder.CAMPOS_PIPELINE
    if pedidos_e_pipeline:
        problemas.append(f"campos do pipeline pedidos ao modelo: {sorted(pedidos_e_pipeline)}")

    for campo, vocab in cb.campos_enum().items():
        if campo in coder.CAMPOS_PIPELINE:
            continue
        prop = coder.EVENT_PROPERTIES[campo]
        got = prop.get("enum") or prop.get("items", {}).get("enum")
        got = {x for x in (got or []) if x is not None}
        if got != vocab:
            problemas.append(f"{campo}: enum diverge do codebook "
                             f"(faltam {sorted(vocab - got)}, sobram {sorted(got - vocab)})")

    prompt = coder.SYSTEM_PROMPT
    if "Registre o MAIOR valor em publico_max" not in prompt:
        problemas.append("system prompt não instrui a registrar o MAIOR valor de público")
    for decisao in cb.aep()["decisoes"]:
        if f"- {decisao}:" not in prompt:
            problemas.append(f"system prompt sem a decisão '{decisao}'")

    if problemas:
        print("DIVERGÊNCIAS:")
        for p in problemas:
            print(f"  - {p}")
        return 1

    print(f"OK: {len(declarados)} variáveis do codebook cobertas "
          f"({len(coder.EVENT_PROPERTIES)} pelo modelo, {len(coder.CAMPOS_PIPELINE)} pelo pipeline); "
          f"enums alinhados; regra de público e {len(cb.aep()['decisoes'])} decisões no prompt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
