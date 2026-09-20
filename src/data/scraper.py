"""01_scraper.py — Coleta de artigos do Acervo Folha via Playwright.

Passagem 1 do protocolo (docs/aep-protocol-bep.md §11). Faz login, itera
termos de busca × janelas temporais (config/queries.yaml), salva cada artigo
como JSON em pipeline/data/raw/ e mantém estado incremental (interrompível).

Os seletores CSS ficam em config/selectors.yaml — editáveis sem tocar em
Python. O Acervo é uma aplicação React e muda de layout sem aviso.

MODOS DE USO
  python 01_scraper.py --diagnose --headed   # PRIMEIRO PASSO: valida seletores
  python 01_scraper.py --dry-run             # lista o que coletaria, sem baixar
  python 01_scraper.py --limit 20            # coleta no máximo 20 artigos
  python 01_scraper.py                       # coleta completa

Comece SEMPRE por --diagnose: sem seletores validados a coleta retorna zero.
"""

import argparse
import hashlib
import json
import os
import random
import time
import urllib.parse
from pathlib import Path

import yaml
from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

load_dotenv()

BASE = Path(__file__).resolve().parent
CFG = yaml.safe_load((BASE / "config" / "queries.yaml").read_text())
SEL = yaml.safe_load((BASE / "config" / "selectors.yaml").read_text())
ROOT = BASE.parent
RAW_DIR = ROOT / "pipeline" / "data" / "raw"
DIAG_DIR = ROOT / "pipeline" / "data" / "diagnose"
STATE_FILE = ROOT / CFG["scraper"]["state_file"]

LOGIN_URL = "https://login.folha.com.br/login"
SEARCH_URL = "https://acervo.folha.com.br/busca.do"

# Identificação honesta do coletor. Scraping acadêmico não se disfarça de
# navegador comum: se o mantenedor do acervo quiser nos contatar ou bloquear,
# deve conseguir.
USER_AGENT = (
    "Mozilla/5.0 (compatible; PesquisaAcademicaAEP/1.0; "
    "projeto de pesquisa sobre ciclos de protesto; contato via repositório)"
)

MAX_PAGES_PER_QUERY = 200   # guarda contra loop infinito de paginação
ARTICLE_RETRIES = 3
NAV_TIMEOUT_MS = 45_000


# ---------------------------------------------------------------------------
# Seletores com candidatos
# ---------------------------------------------------------------------------

def first_match(scope, candidates: list[str]):
    """Primeiro candidato que casar, ou None. Usado para elemento único."""
    for css in candidates:
        try:
            el = scope.query_selector(css)
        except PlaywrightError:
            continue   # seletor sintaticamente inválido: ignora e segue
        if el:
            return el
    return None


def all_matches(scope, candidates: list[str]) -> list:
    """Elementos do primeiro candidato que retornar algo. Lista vazia se nenhum."""
    for css in candidates:
        try:
            els = scope.query_selector_all(css)
        except PlaywrightError:
            continue
        if els:
            return els
    return []


# ---------------------------------------------------------------------------
# Estado
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
        state.setdefault("done", [])
        state.setdefault("pages_done", {})
        return state
    return {"done": [], "pages_done": {}}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def article_path(url: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()[:16]
    return RAW_DIR / f"{h}.json"


# ---------------------------------------------------------------------------
# Navegação
# ---------------------------------------------------------------------------

def search_url(term: str, dr: dict) -> str:
    """URL de busca com parâmetros CODIFICADOS.

    Antes os parâmetros iam crus na URL: termos com acento ('manifestação')
    ou espaço ('ato público') produziam requisição inválida — a coleta
    falharia logo no primeiro termo.
    """
    params = urllib.parse.urlencode({
        "keyword": term,
        "periododesc": f'{dr["start"]} a {dr["end"]}',
    })
    return f"{SEARCH_URL}?{params}"


def login(page) -> None:
    """Faz login e CONFIRMA que deu certo.

    Sem a confirmação, credencial errada ou mudança de layout produziam uma
    coleta de zero artigos sem nenhum erro — o pior modo de falha possível.
    """
    email = os.environ.get("FOLHA_EMAIL")
    password = os.environ.get("FOLHA_PASSWORD")
    if not email or not password:
        raise SystemExit(
            "FOLHA_EMAIL/FOLHA_PASSWORD ausentes. Copie pipeline/.env.example "
            "para pipeline/.env e preencha (o .env nunca é versionado)."
        )

    page.goto(LOGIN_URL, timeout=NAV_TIMEOUT_MS)
    campo_email = first_match(page, SEL["login"]["email"])
    campo_senha = first_match(page, SEL["login"]["password"])
    botao = first_match(page, SEL["login"]["submit"])
    if not (campo_email and campo_senha and botao):
        raise SystemExit(
            "Formulário de login não encontrado — seletores desatualizados.\n"
            "Rode: python 01_scraper.py --diagnose --headed"
        )

    campo_email.fill(email)
    campo_senha.fill(password)
    botao.click()
    page.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)

    if not first_match(page, SEL["login"]["logged_in_marker"]):
        raise SystemExit(
            "Login não confirmado. Causas prováveis: credencial incorreta, "
            "captcha, assinatura expirada, ou o marcador 'logged_in_marker' "
            "em config/selectors.yaml está desatualizado.\n"
            "Rode: python 01_scraper.py --diagnose --headed"
        )
    print("[login] confirmado")


def extract_search_results(page) -> list[dict]:
    """Extrai (url, date_hint) dos resultados da página atual.

    Resolve hrefs relativos contra a URL da página: antes o href ia cru para
    page.goto(), o que falha em todo link relativo.
    """
    results = []
    for item in all_matches(page, SEL["search"]["result_item"]):
        link = first_match(item, SEL["search"]["result_link"])
        if not link:
            continue
        href = link.get_attribute("href")
        if not href:
            continue
        date_el = first_match(item, SEL["search"]["result_date"])
        results.append({
            "url": urllib.parse.urljoin(page.url, href),
            "date_hint": date_el.inner_text().strip() if date_el else None,
        })
    return results


def extract_article_content(page) -> dict:
    title = first_match(page, SEL["article"]["title"])
    body = first_match(page, SEL["article"]["body"])
    return {
        "title": title.inner_text().strip() if title else None,
        "text": body.inner_text().strip() if body else None,
    }


def fetch_article(browser, url: str) -> dict | None:
    """Baixa um artigo com retry e backoff. Fecha a aba sempre.

    O `finally` importa: antes, uma falha em goto() deixava a aba aberta, e
    numa coleta longa o vazamento de abas derrubava o processo.
    """
    for tentativa in range(1, ARTICLE_RETRIES + 1):
        apage = None
        try:
            apage = browser.new_page(user_agent=USER_AGENT)
            apage.goto(url, timeout=NAV_TIMEOUT_MS)
            apage.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)
            return extract_article_content(apage)
        except (PlaywrightTimeout, PlaywrightError) as e:
            espera = 2 ** tentativa + random.uniform(0, 1)
            if tentativa == ARTICLE_RETRIES:
                print(f"  [falha após {ARTICLE_RETRIES} tentativas] {url}: {e}")
                return None
            print(f"  [tentativa {tentativa}] {url}: {type(e).__name__}; "
                  f"aguardando {espera:.1f}s")
            time.sleep(espera)
        finally:
            if apage:
                apage.close()
    return None


# ---------------------------------------------------------------------------
# Diagnóstico de seletores
# ---------------------------------------------------------------------------

def diagnose(browser) -> None:
    """Valida seletores em UMA busca e grava HTML + screenshot.

    Existe porque o modo de falha típico deste scraper é silencioso: layout
    muda, seletor para de casar, coleta retorna zero e nada explica por quê.
    """
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    page = browser.new_page(user_agent=USER_AGENT)
    relatorio = []

    def checar(rotulo: str, scope, candidatos: list[str]) -> int:
        achados = 0
        for css in candidatos:
            try:
                n = len(scope.query_selector_all(css))
            except PlaywrightError:
                relatorio.append(f"  {rotulo:<22} {css!r}: SELETOR INVÁLIDO")
                continue
            marca = "OK " if n else "   "
            relatorio.append(f"  {marca}{rotulo:<22} {css!r}: {n} elemento(s)")
            achados += n
        return achados

    print("\n=== DIAGNÓSTICO DE SELETORES ===\n")

    print("[1/3] Página de login")
    page.goto(LOGIN_URL, timeout=NAV_TIMEOUT_MS)
    relatorio.append("LOGIN:")
    for chave in ("email", "password", "submit"):
        checar(chave, page, SEL["login"][chave])
    (DIAG_DIR / "login.html").write_text(page.content(), encoding="utf-8")
    page.screenshot(path=str(DIAG_DIR / "login.png"), full_page=True)

    print("[2/3] Autenticando")
    try:
        login(page)
        relatorio.append("LOGIN CONFIRMADO: sim")
    except SystemExit as e:
        relatorio.append(f"LOGIN CONFIRMADO: NÃO — {e}")
        print(f"  {e}")

    print("[3/3] Página de busca (primeiro termo × primeira janela)")
    term = CFG["search_terms"][0]
    dr = CFG["date_ranges"][0]
    url = search_url(term, dr)
    relatorio.append(f"\nBUSCA: {url}")
    page.goto(url, timeout=NAV_TIMEOUT_MS)
    page.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)
    (DIAG_DIR / "busca.html").write_text(page.content(), encoding="utf-8")
    page.screenshot(path=str(DIAG_DIR / "busca.png"), full_page=True)

    relatorio.append("BUSCA:")
    n_itens = checar("result_item", page, SEL["search"]["result_item"])
    checar("next_page", page, SEL["search"]["next_page"])

    if n_itens:
        item = first_match(page, SEL["search"]["result_item"])
        relatorio.append("DENTRO DO 1º RESULTADO:")
        checar("result_link", item, SEL["search"]["result_link"])
        checar("result_date", item, SEL["search"]["result_date"])

        resultados = extract_search_results(page)
        relatorio.append(f"\nURLs extraídas da 1ª página: {len(resultados)}")
        for r in resultados[:3]:
            relatorio.append(f"  {r['url']}  (data: {r['date_hint']})")

        if resultados:
            print("      abrindo o primeiro artigo")
            apage = browser.new_page(user_agent=USER_AGENT)
            apage.goto(resultados[0]["url"], timeout=NAV_TIMEOUT_MS)
            apage.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)
            (DIAG_DIR / "artigo.html").write_text(apage.content(), encoding="utf-8")
            apage.screenshot(path=str(DIAG_DIR / "artigo.png"), full_page=True)
            relatorio.append("ARTIGO:")
            checar("title", apage, SEL["article"]["title"])
            checar("body", apage, SEL["article"]["body"])
            conteudo = extract_article_content(apage)
            corpo = conteudo["text"] or ""
            relatorio.append(f"  título extraído: {conteudo['title']!r}")
            relatorio.append(f"  corpo extraído: {len(corpo)} chars")
            if corpo:
                relatorio.append(f"  primeiros 200: {corpo[:200]!r}")
            apage.close()
    else:
        relatorio.append("\n>>> NENHUM RESULTADO CASOU. Abra pipeline/data/diagnose/"
                         "busca.html e ajuste 'search.result_item' em "
                         "config/selectors.yaml.")

    page.close()
    texto = "\n".join(relatorio)
    (DIAG_DIR / "relatorio.txt").write_text(texto, encoding="utf-8")
    print("\n" + texto)
    print(f"\nHTML, screenshots e relatório em: {DIAG_DIR}")
    print("Ajuste config/selectors.yaml e rode o diagnóstico de novo.")


# ---------------------------------------------------------------------------
# Coleta
# ---------------------------------------------------------------------------

def run(limit: int | None, dry_run: bool, headed: bool) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    delay = CFG["scraper"]["delay_seconds"]
    coletados = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        page = browser.new_page(user_agent=USER_AGENT)
        login(page)

        for dr in CFG["date_ranges"]:
            for term in CFG["search_terms"]:
                task_id = f'{dr["label"]}|{term}'
                if task_id in state["done"]:
                    continue
                print(f"[busca] {task_id}")
                page.goto(search_url(term, dr), timeout=NAV_TIMEOUT_MS)
                page.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)

                vistas: set[str] = set()
                for n_pagina in range(1, MAX_PAGES_PER_QUERY + 1):
                    resultados = extract_search_results(page)
                    novas = [r for r in resultados if r["url"] not in vistas]
                    vistas.update(r["url"] for r in resultados)

                    if not novas and n_pagina > 1:
                        # Paginação girando em falso (botão "próxima" sempre
                        # presente, conteúdo repetido). Antes: loop infinito.
                        print(f"  [fim] página {n_pagina} sem resultados novos")
                        break

                    for r in novas:
                        out = article_path(r["url"])
                        if out.exists():
                            continue
                        if limit is not None and coletados >= limit:
                            print(f"  [limite] {limit} artigos atingido")
                            save_state(state)
                            browser.close()
                            return
                        if dry_run:
                            print(f"  [dry-run] {r['url']}")
                            coletados += 1
                            continue
                        conteudo = fetch_article(browser, r["url"])
                        if conteudo is None:
                            continue
                        out.write_text(json.dumps({
                            "url": r["url"],
                            "date_hint": r["date_hint"],
                            "search_term": term,
                            "date_range": dr["label"],
                            **conteudo,
                        }, ensure_ascii=False, indent=2), encoding="utf-8")
                        coletados += 1
                        time.sleep(delay)

                    # Progresso em nível de página: interromper no meio de uma
                    # janela longa não obriga mais a refazer a janela inteira.
                    state["pages_done"][task_id] = n_pagina
                    save_state(state)

                    nxt = first_match(page, SEL["search"]["next_page"])
                    if not nxt:
                        break
                    try:
                        nxt.click()
                        page.wait_for_load_state("networkidle", timeout=NAV_TIMEOUT_MS)
                    except (PlaywrightTimeout, PlaywrightError) as e:
                        print(f"  [paginação interrompida] {type(e).__name__}: {e}")
                        break
                    time.sleep(delay)
                else:
                    print(f"  [aviso] limite de {MAX_PAGES_PER_QUERY} páginas atingido")

                state["done"].append(task_id)
                state["pages_done"].pop(task_id, None)
                save_state(state)

        browser.close()

    rotulo = "listados (dry-run)" if dry_run else "coletados"
    print(f"Coleta concluída. {coletados} artigos {rotulo}. Destino: {RAW_DIR}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--diagnose", action="store_true",
                    help="valida os seletores em uma busca e grava HTML/screenshots")
    ap.add_argument("--dry-run", action="store_true",
                    help="lista as URLs que seriam coletadas, sem baixar")
    ap.add_argument("--limit", type=int, default=None,
                    help="para após N artigos (teste barato)")
    ap.add_argument("--headed", action="store_true",
                    help="abre o navegador visível (necessário para inspecionar)")
    args = ap.parse_args()

    if args.diagnose:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=not args.headed)
            try:
                diagnose(browser)
            finally:
                browser.close()
        return

    run(limit=args.limit, dry_run=args.dry_run, headed=args.headed)


if __name__ == "__main__":
    main()
