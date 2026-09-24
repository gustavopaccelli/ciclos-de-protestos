#!/usr/bin/env python3
"""Initialize SQLite database with DoCA schema for protest events collection."""

import sqlite3
import json
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "protest_events.db"
CODEBOOK_PATH = BASE_DIR.parent / "config" / "doca_codebook.yaml"

def init_database():
    """Create tables for DoCA protest events data."""

    # Load codebook for validation
    codebook = yaml.safe_load(CODEBOOK_PATH.read_text())

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

    # 2. Protest events (main table after DoCA coding)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protest_events (
        event_id TEXT PRIMARY KEY,
        event_date TEXT NOT NULL,
        end_date TEXT,
        duration_days INTEGER,

        -- Location
        location_city TEXT NOT NULL,
        location_state TEXT NOT NULL,
        city_size TEXT CHECK(city_size IN ('pequeno', 'medio', 'grande')),
        location_venue TEXT,
        location_venue_type TEXT NOT NULL,
        location_conventional BOOLEAN,

        -- Crowd
        crowd_size_reported INTEGER,
        crowd_size_min INTEGER,
        crowd_size_max INTEGER,
        crowd_size_scale TEXT CHECK(crowd_size_scale IN ('0', '1', '2', '3', '4', '5')),
        crowd_size_bep TEXT CHECK(crowd_size_bep IN ('pequena', 'media', 'grande', 'mega')),

        -- Claims and political content
        claim_code TEXT NOT NULL,
        claim_text TEXT,
        valence TEXT CHECK(valence IN ('01', '02', '03')),

        -- Repertoires and performances
        repertoire TEXT NOT NULL,
        action_object TEXT,
        action_instrument TEXT,

        -- Conflict and repression
        conflict_present BOOLEAN,
        repression TEXT CHECK(repression IN ('none', 'dispersão', 'prisões', 'violência')),
        conflict_police BOOLEAN,
        conflict_inter_group BOOLEAN,
        arrests_reported INTEGER,
        injuries_reported INTEGER,

        -- Source tracking
        source_url TEXT,
        source_date TEXT,
        article_desc TEXT,
        event_desc TEXT,
        eligible BOOLEAN DEFAULT TRUE,

        -- Multi-source deduplication
        canonical_event_id TEXT,
        multi_event_article BOOLEAN,
        counter_protest BOOLEAN,

        -- Metadata
        coded_by TEXT,
        coded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (source_url) REFERENCES raw_articles(source_url)
    )
    """)

    # 3. Actors/organizations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actors (
        actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        actor_name TEXT NOT NULL,
        actor_specification TEXT,
        org_type TEXT NOT NULL,
        formalization TEXT CHECK(formalization IN ('formal', 'informal')),

        FOREIGN KEY (event_id) REFERENCES protest_events(event_id) ON DELETE CASCADE
    )
    """)

    # 4. Symbols and slogans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symbols_slogans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        type TEXT CHECK(type IN ('symbol', 'slogan')),
        content TEXT NOT NULL,

        FOREIGN KEY (event_id) REFERENCES protest_events(event_id) ON DELETE CASCADE
    )
    """)

    # 5. SMOs (Formal protest organizations identified)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smos (
        smo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        smo_name TEXT NOT NULL,
        smo_type TEXT,

        FOREIGN KEY (event_id) REFERENCES protest_events(event_id) ON DELETE CASCADE
    )
    """)

    # 6. Codebook reference tables for validation/lookup
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

    # Create indexes for common queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_date ON protest_events(event_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_city ON protest_events(location_city, location_state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claim_code ON protest_events(claim_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_repertoire ON protest_events(repertoire)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_url ON protest_events(source_url)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_canonical ON protest_events(canonical_event_id)")

    conn.commit()
    conn.close()

    print(f"✓ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    init_database()
