#!/usr/bin/env python3
"""Load Folha archive articles into DoCA database structure."""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # noqa: E402
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = paths.DB_PATH
ACERVO_JSON = paths.ACERVO_JSON

def parse_date(date_str: str) -> Optional[str]:
    """Try to parse date strings in various Brazilian formats."""
    if not date_str or date_str.lower() in ("data não informada", "si", ""):
        return None

    date_str = date_str.strip()
    formats = [
        "%d/%m/%Y",
        "%d de %B de %Y",
        "%d de %b de %Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
    ]

    months_pt = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
        "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
        "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12",
        "jan": "01", "fev": "02", "mar": "03", "abr": "04",
        "mai": "05", "jun": "06", "jul": "07", "ago": "08",
        "set": "09", "out": "10", "nov": "11", "dez": "12",
    }

    # Try direct parsing
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Try month substitution (pt-BR format)
    normalized = date_str.lower()
    for pt_month, num_month in months_pt.items():
        normalized = normalized.replace(pt_month, num_month)

    for fmt in formats:
        try:
            dt = datetime.strptime(normalized, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None

def create_event_id(source_url: str, event_date: str, location_city: str = "Unknown") -> str:
    """Generate deterministic UUID5 for event (per DoCA spec)."""
    namespace = uuid.UUID("7c0e4d9a-1984-1992-2013-201520160001")
    event_key = f"{source_url}|{event_date}|{location_city}"
    return str(uuid.uuid5(namespace, event_key))

def load_acervo_articles() -> List[Dict]:
    """Load articles from scraped JSON."""
    if not ACERVO_JSON.exists():
        print(f"⚠ No data found at {ACERVO_JSON}")
        return []

    with open(ACERVO_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "articles" in data:
        return data.get("articles", [])
    elif isinstance(data, list):
        return data
    else:
        print(f"⚠ Unexpected data structure in {ACERVO_JSON}")
        return []

def ingest_articles_to_db(articles: List[Dict]) -> int:
    """Grava as matérias coletadas na tabela raw_articles."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for article in articles:
        try:
            # Parse article metadata
            source_url = article.get("link", "").strip()
            if not source_url:
                skipped += 1
                continue

            title = article.get("titulo", "").strip()
            raw_date = article.get("data", "")
            parsed_date = parse_date(raw_date)

            if not parsed_date:
                parsed_date = datetime.now().strftime("%Y-%m-%d")

            article_id = create_event_id(source_url, parsed_date)

            # Só a matéria bruta entra aqui. Os eventos são criados pelo
            # coder (src/preprocessing/coder.py) depois da leitura do texto;
            # antes este passo inventava um evento por matéria com cidade,
            # tema e repertório padrão, o que contaminaria o banco.
            cursor.execute("""
                INSERT OR IGNORE INTO raw_articles
                (article_id, source_url, source_date, title, publication)
                VALUES (?, ?, ?, ?, ?)
            """, (
                article_id,
                source_url,
                parsed_date,
                title,
                "Folha de São Paulo"
            ))

            inserted += 1

        except Exception as e:
            print(f"✗ Error processing article: {e}")
            skipped += 1

    conn.commit()
    conn.close()

    return inserted

def main():
    """Main workflow: load articles into database."""

    print("=== Loading Folha Acervo into DoCA Database ===\n")

    # Ensure database exists
    if not DB_PATH.exists():
        print(f"📦 Initializing database at {DB_PATH}")
        from init_doca_database import init_database
        init_database()

    # Load articles
    print(f"📖 Loading articles from {ACERVO_JSON}")
    articles = load_acervo_articles()

    if not articles:
        print("⚠ No articles to load.")
        return

    print(f"✓ Loaded {len(articles)} articles")

    # Ingest to database
    print("\n💾 Ingesting into raw_articles table...")
    inserted = ingest_articles_to_db(articles)

    print(f"\n✓ Ingestion complete:")
    print(f"  - Inserted: {inserted} records")
    print(f"  - Database: {DB_PATH}")

    # Summary statistics
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM raw_articles")
    raw_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM protest_events")
    coded_count = cursor.fetchone()[0]

    conn.close()

    print(f"  - Total raw articles: {raw_count}")
    print(f"  - Eventos codificados: {coded_count}")

if __name__ == "__main__":
    main()
