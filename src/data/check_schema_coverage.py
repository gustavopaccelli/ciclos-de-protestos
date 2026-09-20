"""check_schema_coverage.py — Confere o coder contra o codebook.

Verifica que o `EVENT_SCHEMA` implementado em 02_doca_coder.py cobre todos os
campos declarados em `event_schema` de config/doca_codebook.yaml, e que os
enums do schema usam os vocabulários do codebook.

Este teste existe porque a divergência entre os dois era invisível: o coder
implementava ~16 dos ~40 campos declarados, e nada acusava a falta.

Uso: python check_schema_coverage.py     (código de saída 1 se houver divergência)
"""

import importlib.util
import sys
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent


def load_coder():
    spec = importlib.util.spec_from_file_location("doca_coder", BASE / "02_doca_coder.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    codebook = yaml.safe_load((BASE / "config" / "doca_codebook.yaml").read_text())
    coder = load_coder()

    declared = set(codebook["event_schema"])
    implemented = set(coder.EVENT_PROPERTIES) | coder.PIPELINE_ASSIGNED_FIELDS

    faltando = declared - implemented
    extras = implemented - declared - coder.PIPELINE_ASSIGNED_FIELDS

    problemas = []
    if faltando:
        problemas.append(f"campos do codebook NÃO implementados: {sorted(faltando)}")
    if extras:
        problemas.append(f"campos implementados fora do codebook: {sorted(extras)}")

    # Enums devem espelhar o codebook, não listas paralelas.
    esperados = {
        "claim_code": set(codebook["claim_codes"]),
        "repertoire": set(codebook["repertoires"]),
        "repression": set(codebook["repression_levels"]),
        "crowd_size_scale": set(codebook["crowd_size_scale"]),
        "valence": set(codebook["valences"]),
        "target": set(codebook["mpeds_target_categories"]),
        "location_venue_type": set(codebook["location_venue_types"]),
    }
    for field, vocab in esperados.items():
        got = coder.EVENT_PROPERTIES.get(field, {}).get("enum")
        if got is None:
            problemas.append(f"{field}: sem enum no schema")
        elif set(got) != vocab:
            problemas.append(f"{field}: enum diverge do codebook "
                             f"(faltam {sorted(vocab - set(got))}, "
                             f"sobram {sorted(set(got) - vocab)})")

    # A regra de público precisa dizer "maior" — a contradição anterior
    # (prompt dizia "menor") enviesava toda variável derivada de tamanho.
    prompt = coder.SYSTEM_PROMPT
    if "MAIOR valor em crowd_size_reported" not in prompt:
        problemas.append("system prompt não instrui a registrar o MAIOR valor de público")

    if problemas:
        print("DIVERGÊNCIAS:")
        for p in problemas:
            print(f"  - {p}")
        return 1

    print(f"OK: {len(declared)} campos do codebook cobertos pelo coder; "
          f"enums alinhados; regra de público correta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
