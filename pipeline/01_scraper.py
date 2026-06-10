"""01_scraper.py — Coleta de artigos do Acervo Folha via Playwright.

Faz login, itera termos de busca × janelas temporais (config/queries.yaml),
salva cada artigo como JSON em pipeline/data/raw/ e mantém estado incremental
(pode ser interrompido e retomado).

ATENÇÃO: o Acervo Folha é uma aplicação React e muda de layout. Se a coleta
retornar zero artigos, inspecione o HTML (F12 → Elements) e atualize os
seletores CSS em extract_search_results() e extract_article_content().
"""

import hashlib
import json
import os
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

BASE = Path(__file__).resolve().parent
CFG = yaml.safe_load((BASE / "config" / "queries.yaml").read_text())
ROOT = BASE.parent  # raiz do repositório
RAW_DIR = ROOT / "pipeline" / "data" / "raw"
STATE_FILE = ROOT / CFG["scraper"]["state_file"]

LOGIN_URL = "https://login.folha.com.br/login"
SEARCH_URL = "https://acervo.folha.com.br/busca.do"

# --- Seletores CSS centralizados (atualizar aqui se o layout mudar) ---
SEL = {
    "login_email": 'input[name="email"]',
    "login_password": 'input[name="password"]',
    "login_submit": 'button[type="submit"]',
    "result_item": ".resultado-busca .item, article.result",
    "result_link": "a",
    "result_date": ".data, time",
    "article_title": "h1",
    "article_body": ".content, .news, article",
    "next_page": 'a[rel="next"], .paginacao .proxima',
}


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def article_path(url: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()[:16]
    return RAW_DIR / f"{h}.json"


def login(page) -> None:
    page.goto(LOGIN_URL)
    page.fill(SEL["login_email"], os.environ["FOLHA_EMAIL"])
    page.fill(SEL["login_password"], os.environ["FOLHA_PASSWORD"])
    page.click(SEL["login_submit"])
    page.wait_for_load_state("networkidle")


def extract_search_results(page) -> list[dict]:
    """Extrai (url, data) dos resultados da página atual de busca."""
    results = []
    for item in page.query_selector_all(SEL["result_item"]):
        link = item.query_selector(SEL["result_link"])
        date_el = item.query_selector(SEL["result_date"])
        if link:
            results.append({
                "url": link.get_attribute("href"),
                "date_hint": date_el.inner_text().strip() if date_el else None,
            })
    return results


def extract_article_content(page) -> dict:
    title = page.query_selector(SEL["article_title"])
    body = page.query_selector(SEL["article_body"])
    return {
        "title": title.inner_text().strip() if title else None,
        "text": body.inner_text().strip() if body else None,
    }


def run() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    delay = CFG["scraper"]["delay_seconds"]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        login(page)

        for dr in CFG["date_ranges"]:
            for term in CFG["search_terms"]:
                task_id = f'{dr["label"]}|{term}'
                if task_id in state["done"]:
                    continue
                print(f"[busca] {task_id}")
                page.goto(
                    f'{SEARCH_URL}?keyword={term}'
                    f'&periododesc={dr["start"]}+a+{dr["end"]}'
                )
                page.wait_for_load_state("networkidle")

                while True:
                    for r in extract_search_results(page):
                        out = article_path(r["url"])
                        if out.exists():
                            continue
                        try:
                            apage = browser.new_page()
                            apage.goto(r["url"])
                            apage.wait_for_load_state("networkidle")
                            content = extract_article_content(apage)
                            apage.close()
                            out.write_text(json.dumps({
                                "url": r["url"],
                                "date_hint": r["date_hint"],
                                "search_term": term,
                                "date_range": dr["label"],
                                **content,
                            }, ensure_ascii=False, indent=2))
                            time.sleep(delay)
                        except Exception as e:  # rede instável: registra e segue
                            print(f"  [erro] {r['url']}: {e}")
                    nxt = page.query_selector(SEL["next_page"])
                    if not nxt:
                        break
                    nxt.click()
                    page.wait_for_load_state("networkidle")
                    time.sleep(delay)

                state["done"].append(task_id)
                save_state(state)

        browser.close()
    print(f"Coleta concluída. Artigos em {RAW_DIR}")


if __name__ == "__main__":
    run()
