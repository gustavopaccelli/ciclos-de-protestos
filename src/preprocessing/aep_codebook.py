"""Leitura do codebook AEP-BR — fonte única de verdade para coder, dataset e kappa.

bancos/03_aep_br/codebook/codebook_aep_br.yaml declara as variáveis; os
vocabulários que ele herda (repertórios, claim_codes etc.) continuam em
config/doca_codebook.yaml. Este módulo junta os dois e oferece consultas por
tipo de variável, para que nenhum script mantenha lista paralela de campos.
"""
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402

import yaml

# Variáveis preenchidas pelo pipeline, nunca pelo modelo nem pelo codificador
# humano: identificadores, derivações determinísticas e metadados de execução.
CAMPOS_PIPELINE = {
    "evento_id", "evento_canonico_id", "ciclo", "fase", "codificador",
    "modelo_versao", "cidade_ibge", "porte_cidade", "n_fontes",
}

# Vocabulários que são documentação, não lista fechada de valores.
_VOCAB_ABERTO = {"base_social"}


@lru_cache(maxsize=1)
def aep() -> dict:
    return yaml.safe_load(paths.AEP_CODEBOOK.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def doca() -> dict:
    return yaml.safe_load((paths.RAIZ / aep()["vocabularios_herdados"]).read_text(encoding="utf-8"))


def vocab_bruto(nome: str):
    """Vocabulário como está no YAML (dict com definições ou lista)."""
    proprios = aep()["vocabularios"]
    if nome in proprios:
        return proprios[nome]
    return doca()[nome]


def valores(nome: str) -> list[str] | None:
    """Valores permitidos de um vocabulário fechado; None se for aberto."""
    if nome in _VOCAB_ABERTO:
        return None
    v = vocab_bruto(nome)
    if isinstance(v, dict):
        return [str(k) for k in v]
    return [str(x) for x in v]


def variaveis() -> list[dict]:
    return aep()["variaveis"]


def variavel(nome: str) -> dict:
    return next(v for v in variaveis() if v["nome"] == nome)


def nomes(tipo: str | None = None) -> list[str]:
    return [v["nome"] for v in variaveis() if tipo is None or v["tipo"] == tipo]


def campos_enum() -> dict[str, set[str]]:
    """Variáveis com vocabulário fechado (escalares e listas) → valores."""
    out = {}
    for v in variaveis():
        voc = v.get("vocabulario")
        if voc and v["tipo"] in ("enum", "list[str]") and valores(voc) is not None:
            out[v["nome"]] = set(valores(voc))
    return out


def campos_lista() -> list[str]:
    return [v["nome"] for v in variaveis() if v["tipo"].startswith("list[")]


def limiar_kappa() -> float:
    return aep()["confiabilidade"]["kappa_minimo"]


def limiar_missing() -> float:
    return aep()["confiabilidade"]["exclusao_missing"]
