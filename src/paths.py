"""Caminhos centrais do repositório.

Os scripts importam daqui em vez de montar caminhos relativos ao próprio
arquivo, que quebraram na reorganização de 2026-09.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CONFIG = RAIZ / "config"
DOCS = RAIZ / "docs"

# Um diretório por banco de dados (ver bancos/README.md)
BANCOS = RAIZ / "bancos"
MM = BANCOS / "01_mass_mobilization"
NEPAC = BANCOS / "02_nepac"
AEP_BR = BANCOS / "03_aep_br"
AEP_CODEBOOK = AEP_BR / "codebook" / "codebook_aep_br.yaml"
AEP_SEMENTES = AEP_BR / "sementes"
AEP_COLETA = AEP_BR / "coleta"
FOLHA_RAW = AEP_COLETA / "folha_acervo"
ACERVO_JSON = AEP_COLETA / "acervo_protestos.json"
DB_PATH = AEP_BR / "protest_events.db"

# Dados derivados
DATA = RAIZ / "data"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
TRIANGULACAO = DATA / "triangulacao"

# Bibliografia e process tracing
BIB = DOCS / "artigo" / "referencias.bib"
ABNT = DOCS / "artigo" / "referencias-abnt.md"
PROCESS_TRACING = DOCS / "process_tracing"
