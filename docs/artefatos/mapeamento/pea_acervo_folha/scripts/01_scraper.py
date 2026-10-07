#!/usr/bin/env python3
"""
=============================================================
scripts/01_scraper.py
Extração de artigos do Acervo Folha de S.Paulo
Utiliza Playwright (browser headless) para contornar
renderização JavaScript dinâmica do acervo.

ATENÇÃO: Respeite os Termos de Uso do Acervo Folha.
Use exclusivamente para fins de pesquisa acadêmica
com credenciais próprias e válidas.
=============================================================
"""

import os
import time
import json
import logging
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

# --- Configuração inicial ---
load_dotenv()
BASE_DIR   = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
RAW_DIR    = OUTPUT_DIR / "raw_articles"
LOG_DIR    = OUTPUT_DIR / "logs"

for d in [RAW_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == "true" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# --- Carrega configurações ---
with open(BASE_DIR / "config" / "queries.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

FOLHA_EMAIL    = os.getenv("FOLHA_EMAIL")
FOLHA_PASSWORD = os.getenv("FOLHA_PASSWORD")
START_DATE     = datetime.strptime(os.getenv("START_DATE", "1985-01-01"), "%Y-%m-%d")
END_DATE       = datetime.strptime(os.getenv("END_DATE", "2024-12-31"), "%Y-%m-%d")
REQUEST_DELAY  = float(os.getenv("REQUEST_DELAY", "3"))
MAX_ARTICLES   = int(os.getenv("MAX_ARTICLES", "0"))

ACERVO_BASE  = cfg["acervo_base_url"]
SEARCH_URL   = ACERVO_BASE + cfg["search_endpoint"]
LOGIN_URL    = cfg["login_url"]


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def make_article_id(date_str: str, title: str, url: str) -> str:
    """Gera ID determinístico baseado em data + título + url."""
    raw = f"{date_str}|{title}|{url}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def polite_sleep(base: float = REQUEST_DELAY) -> None:
    """Pausa com jitter aleatório para evitar detecção de bot."""
    jitter = random.uniform(0.5, 1.5)
    time.sleep(base * jitter)


def already_scraped(article_id: str) -> bool:
    """Verifica se artigo já foi coletado (evita duplicatas em execuções parciais)."""
    return (RAW_DIR / f"{article_id}.json").exists()


def save_article(article: dict) -> None:
    """Salva artigo individual como JSON."""
    path = RAW_DIR / f"{article['article_id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    log.debug(f"Salvo: {article['article_id']} — {article['title'][:60]}")


def load_progress() -> set:
    """Retorna conjunto de IDs já coletados."""
    return {p.stem for p in RAW_DIR.glob("*.json")}


# ─────────────────────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────────────────────

def login(page) -> bool:
    """Realiza login no portal Folha e verifica sucesso."""
    log.info("Realizando login no Acervo Folha...")
    try:
        page.goto(LOGIN_URL, timeout=30_000)
        page.wait_for_load_state("networkidle")

        # Preenche email
        page.fill('input[name="email"], input[type="email"]', FOLHA_EMAIL)
        polite_sleep(1)

        # Preenche senha
        page.fill('input[name="password"], input[type="password"]', FOLHA_PASSWORD)
        polite_sleep(0.5)

        # Clica em entrar
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state("networkidle", timeout=20_000)

        # Verifica se login foi bem-sucedido verificando ausência do formulário
        if "login" not in page.url.lower():
            log.info("Login realizado com sucesso.")
            return True
        else:
            log.error("Falha no login. Verifique FOLHA_EMAIL e FOLHA_PASSWORD no .env")
            return False

    except PWTimeoutError:
        log.error("Timeout durante o login.")
        return False


# ─────────────────────────────────────────────────────────────
# Construção de URL de busca
# ─────────────────────────────────────────────────────────────

def build_search_url(term: str, date_from: datetime, date_to: datetime, page_num: int = 1) -> str:
    """
    Monta URL de busca do Acervo Folha.
    Parâmetros inferidos da interface do acervo (inspecionar via DevTools se mudarem).
    """
    from urllib.parse import urlencode
    params = {
        "q":        term,
        "site":     "jornal_acervo",
        "period":   "specific",
        "startDate": date_from.strftime("%d/%m/%Y"),
        "endDate":   date_to.strftime("%d/%m/%Y"),
        "page":      page_num,
    }
    return f"{SEARCH_URL}?{urlencode(params)}"


# ─────────────────────────────────────────────────────────────
# Extração de resultados de uma página de busca
# ─────────────────────────────────────────────────────────────

def extract_search_results(page) -> list[dict]:
    """
    Extrai links e metadados básicos dos resultados de uma
    página de busca do Acervo Folha.
    Adapte os seletores CSS se o layout mudar.
    """
    results = []
    try:
        # Aguarda carregamento dos resultados
        page.wait_for_selector(".search-result-item, .result-item, article.news", timeout=15_000)
    except PWTimeoutError:
        log.warning("Nenhum resultado encontrado nesta página ou seletor desatualizado.")
        return results

    items = page.query_selector_all(
        ".search-result-item, .result-item, article.news, .c-search-result__item"
    )
    for item in items:
        try:
            # Título e link
            title_el = item.query_selector("h2 a, h3 a, .c-headline__title a, a.title")
            if not title_el:
                continue
            title = title_el.inner_text().strip()
            href  = title_el.get_attribute("href") or ""
            if href and not href.startswith("http"):
                href = ACERVO_BASE + href

            # Data de publicação
            date_el = item.query_selector("time, .date, .c-more__date, span.pubdate")
            pub_date = date_el.get_attribute("datetime") or date_el.inner_text() if date_el else ""

            # Trecho / resumo
            snippet_el = item.query_selector("p.summary, .c-headline__standfirst, p.description")
            snippet = snippet_el.inner_text().strip() if snippet_el else ""

            # Editoria / seção
            section_el = item.query_selector(".section, .caderno, .c-headline__kicker")
            section = section_el.inner_text().strip() if section_el else ""

            results.append({
                "title":    title,
                "url":      href,
                "pub_date": pub_date,
                "snippet":  snippet,
                "section":  section,
            })
        except Exception as e:
            log.debug(f"Erro ao extrair item: {e}")
            continue

    return results


def has_next_page(page) -> bool:
    """Verifica se há próxima página de resultados."""
    next_btn = page.query_selector("a[rel='next'], .pagination__next, button.next-page")
    return next_btn is not None and next_btn.is_visible()


# ─────────────────────────────────────────────────────────────
# Extração do conteúdo completo de um artigo
# ─────────────────────────────────────────────────────────────

def extract_article_content(page, url: str, meta: dict) -> dict | None:
    """Acessa o artigo completo e extrai texto, autor e metadados."""
    try:
        page.goto(url, timeout=30_000)
        page.wait_for_load_state("domcontentloaded")
        polite_sleep(1)

        # Título
        title_el = page.query_selector("h1.c-content-head__title, h1.title, h1")
        title = title_el.inner_text().strip() if title_el else meta.get("title", "")

        # Subtítulo / chapéu
        subtitle_el = page.query_selector(".c-content-head__subtitle, .subtitulo, h2.subheadline")
        subtitle = subtitle_el.inner_text().strip() if subtitle_el else ""

        # Corpo do texto
        body_els = page.query_selector_all(
            "p.c-news__body-text, div.news-content p, .news-body p, article p"
        )
        body = "\n".join(el.inner_text().strip() for el in body_els if el.inner_text().strip())

        # Autor
        author_el = page.query_selector(".c-content-head__author, .author, .byline, span.author")
        author = author_el.inner_text().strip() if author_el else ""

        # Data estruturada
        date_el = page.query_selector("time[datetime]")
        pub_date = date_el.get_attribute("datetime") if date_el else meta.get("pub_date", "")

        # Seção / caderno
        section_el = page.query_selector(".c-headline__kicker, .section, .caderno")
        section = section_el.inner_text().strip() if section_el else meta.get("section", "")

        article_id = make_article_id(pub_date, title, url)

        return {
            "article_id": article_id,
            "url":        url,
            "title":      title,
            "subtitle":   subtitle,
            "author":     author,
            "pub_date":   pub_date,
            "section":    section,
            "body":       body,
            "source":     "Folha de S.Paulo / Acervo",
            "scraped_at": datetime.utcnow().isoformat(),
        }

    except PWTimeoutError:
        log.warning(f"Timeout ao acessar artigo: {url}")
        return None
    except Exception as e:
        log.error(f"Erro ao extrair artigo {url}: {e}")
        return None


# ─────────────────────────────────────────────────────────────
# Filtro de elegibilidade pré-codificação
# ─────────────────────────────────────────────────────────────

EXCLUSION_TERMS = [t.lower() for t in cfg.get("exclusion_terms", [])]
INCLUDE_SECTIONS = [s.lower() for s in cfg.get("include_sections", [])]
EXCLUDE_SECTIONS = [s.lower() for s in cfg.get("exclude_sections", [])]


def is_eligible_candidate(article: dict) -> bool:
    """
    Triagem rápida antes da codificação por LLM.
    Descarta falsos positivos óbvios por seção e termos de exclusão.
    """
    section_low = article.get("section", "").lower()
    if any(ex in section_low for ex in EXCLUDE_SECTIONS):
        return False

    combined = (article.get("title", "") + " " + article.get("body", "")).lower()
    if any(ex_term in combined for ex_term in EXCLUSION_TERMS):
        # Artigo pode ainda ser válido se tiver termos de protesto fortes
        contention_hits = sum(
            1 for t in ["manifestação", "protesto", "marcha", "greve", "ocupação", "passeata"]
            if t in combined
        )
        if contention_hits < 2:
            return False

    return True


# ─────────────────────────────────────────────────────────────
# Orquestrador principal
# ─────────────────────────────────────────────────────────────

def run_scraper():
    """Executa o scraper completo para todas as queries e período definido."""
    already_done = load_progress()
    log.info(f"Retomando coleta. Artigos já coletados: {len(already_done)}")

    # Monta lista de termos combinados para busca
    primary_terms = (
        cfg["query_groups"]["contention_terms"]
        + cfg["query_groups"]["strike_terms"]
        + cfg["query_groups"]["mobilization_terms"]
    )
    # Remove duplicatas mantendo ordem
    seen = set()
    search_terms = [t for t in primary_terms if not (t in seen or seen.add(t))]

    total_collected = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        page = context.new_page()

        # --- Login ---
        if not login(page):
            browser.close()
            return

        # --- Iteração por termo de busca ---
        for term in search_terms:
            log.info(f"Buscando por: '{term}'")
            page_num = 1

            while True:
                url = build_search_url(term, START_DATE, END_DATE, page_num)
                log.debug(f"  Página {page_num}: {url}")

                try:
                    page.goto(url, timeout=30_000)
                    page.wait_for_load_state("networkidle")
                except PWTimeoutError:
                    log.warning(f"Timeout na página de resultados. Pulando.")
                    break

                results = extract_search_results(page)
                if not results:
                    log.info(f"  Sem mais resultados para '{term}' na página {page_num}.")
                    break

                for meta in results:
                    if MAX_ARTICLES and total_collected >= MAX_ARTICLES:
                        log.info("Limite MAX_ARTICLES atingido. Encerrando.")
                        browser.close()
                        return

                    article_id = make_article_id(
                        meta.get("pub_date", ""), meta.get("title", ""), meta.get("url", "")
                    )
                    if article_id in already_done:
                        log.debug(f"  Já coletado: {article_id}")
                        continue

                    polite_sleep(REQUEST_DELAY)
                    article = extract_article_content(page, meta["url"], meta)

                    if article and is_eligible_candidate(article):
                        save_article(article)
                        already_done.add(article["article_id"])
                        total_collected += 1
                        log.info(
                            f"  [{total_collected}] {article['pub_date'][:10]} — "
                            f"{article['title'][:70]}"
                        )

                if not has_next_page(page):
                    break
                page_num += 1
                polite_sleep(REQUEST_DELAY * 1.5)

        browser.close()

    log.info(f"Coleta encerrada. Total de artigos novos coletados: {total_collected}")
    log.info(f"Total acumulado no diretório: {len(list(RAW_DIR.glob('*.json')))}")


if __name__ == "__main__":
    run_scraper()
