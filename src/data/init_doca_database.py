#!/usr/bin/env python3
"""Cria o banco SQLite do AEP-BR (bancos/03_aep_br/protest_events.db).

A tabela protest_events é gerada a partir das variáveis de
bancos/03_aep_br/codebook/codebook_aep_br.yaml: não há lista paralela de
colunas. Os vocabulários de referência (temas, repertórios) vêm de
config/doca_codebook.yaml.
"""

import sqlite3
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402
sys.path.insert(0, str(paths.RAIZ / "src" / "preprocessing"))
import aep_codebook as cb  # noqa: E402

DB_PATH = paths.DB_PATH

_SQL = {"date": "TEXT", "str": "TEXT", "enum": "TEXT", "int": "INTEGER", "bool": "BOOLEAN"}


def _ddl_eventos() -> str:
    linhas = []
    for v in cb.variaveis():
        tipo = "TEXT" if v["tipo"].startswith("list[") else _SQL[v["tipo"]]
        if v["nome"] == "evento_id":
            linhas.append("evento_id TEXT PRIMARY KEY")
            continue
        restr = ""
        vals = cb.valores(v["vocabulario"]) if v["tipo"] == "enum" and v.get("vocabulario") else None
        if vals:
            lista = ", ".join("'" + x.replace("'", "''") + "'" for x in vals)
            restr = f" CHECK({v['nome']} IN ({lista}))"
        linhas.append(f"{v['nome']} {tipo}{restr}")
    linhas.append("codificado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    return "CREATE TABLE IF NOT EXISTS protest_events (\n    " + ",\n    ".join(linhas) + "\n)"

def init_database():
    """Cria as tabelas do banco AEP-BR."""

    codebook = cb.doca()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # 1. Raw articles table (from scraper)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_articles (
        article_id TEXT PRIMARY KEY,
        source_url TEXT UNIQUE NOT NULL,
        source_date TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT,
        publication TEXT,
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Eventos — uma coluna por variável do codebook AEP-BR. Listas e objetos
    # (atores, fontes, tema_codigo...) ficam como JSON em TEXT.
    cursor.execute(_ddl_eventos())

    # 3. Tabelas de referência dos vocabulários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS codebook_claims (
        claim_code TEXT PRIMARY KEY,
        claim_description TEXT NOT NULL,
        domain TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS codebook_repertoires (
        repertoire TEXT PRIMARY KEY,
        description TEXT
    )
    """)

    # Populate codebook reference tables
    for code, desc in codebook.get("claim_codes", {}).items():
        domain = code[0:2]  # First two digits = domain
        cursor.execute(
            "INSERT OR IGNORE INTO codebook_claims VALUES (?, ?, ?)",
            (code, desc, domain)
        )

    for repertoire in codebook.get("repertoires", []):
        cursor.execute(
            "INSERT OR IGNORE INTO codebook_repertoires VALUES (?, ?)",
            (repertoire, None)
        )

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_data ON protest_events(data_inicio)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cidade ON protest_events(cidade, uf)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ciclo ON protest_events(ciclo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_canonico ON protest_events(evento_canonico_id)")

    conn.commit()
    conn.close()

    print(f"✓ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    init_database()
