#!/usr/bin/env python3
"""
=============================================================
scripts/02_doca_coder.py
Codificação automática de eventos de protesto via API Claude.

Para cada artigo bruto coletado pelo scraper, este script:
  1. Avalia elegibilidade DoCA
  2. Identifica e delimita eventos (regras temporal/espacial/agencial)
  3. Extrai todas as variáveis do schema JSON especificado
  4. Salva resultado em output/coded_events/

Requer: ANTHROPIC_API_KEY no arquivo .env
=============================================================
"""

import os
import json
import time
import uuid
import logging
import hashlib
from pathlib import Path
from datetime import datetime

import anthropic
from dotenv import load_dotenv

# --- Setup ---
load_dotenv()
BASE_DIR     = Path(__file__).parent.parent
OUTPUT_DIR   = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
RAW_DIR      = OUTPUT_DIR / "raw_articles"
CODED_DIR    = OUTPUT_DIR / "coded_events"
REJECTED_DIR = OUTPUT_DIR / "rejected_articles"
LOG_DIR      = OUTPUT_DIR / "logs"

for d in [CODED_DIR, REJECTED_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == "true" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "coder.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ─────────────────────────────────────────────────────────────
# Prompts
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é um Cientista Político Computacional especializado em
Análise de Eventos de Protesto (PEA) seguindo o protocolo DoCA
(Dynamics of Collective Action — McAdam, Tarrow, Tilly).

Sua tarefa: analisar artigos da imprensa brasileira e extrair eventos
de protesto estruturados.

## CRITÉRIOS DE ELEGIBILIDADE DoCA

INCLUIR se o evento:
1. Tem participação direta de MAIS DE UM indivíduo simultaneamente
2. Ocorre em espaço de acesso público ou visível publicamente
3. Articula publicamente uma reivindicação, queixa ou posicionamento
   em favor/oposição a mudança estrutural ou política estatal
4. EXCEÇÃO: agressões motivadas por ódio racial/étnico/gênero são
   codificadas mesmo sem demanda explícita dos agressores

EXCLUIR:
- Eventos iniciados por governo/legisladores/partidos no exercício parlamentar
- Negociações sindicais internas, audiências fechadas, conferências privadas
- Captação de recursos comerciais para campanhas

## REGRAS DE DELIMITAÇÃO DE EVENTOS

Temporal: separar eventos com >24h de inatividade (exceto greves em curso,
que podem ter pausas de fim de semana sob o mesmo ID)

Espacial: eventos em municípios diferentes = eventos separados,
mesmo que sincronizados (mesma campanha)

Agencial: grupos com reivindicações opostas no mesmo espaço = eventos separados

## CLAIM CODES (4 dígitos)

Domínios principais:
10xx = Direitos políticos e democracia
  1001=Sufrágio/eleições diretas, 1002=Impeachment/cassação,
  1003=Reforma política, 1004=Anticorrupção, 1005=Liberdades civis,
  1006=Independência judiciária, 1007=Defesa da democracia, 1008=Autoritarismo

11xx = Direitos trabalhistas e econômicos
  1101=Reajuste salarial, 1102=Reforma trabalhista (contra), 1103=Greve,
  1104=Privatização (contra), 1105=Reforma previdenciária (contra),
  1106=Política fiscal/cortes, 1107=Precarização, 1108=Neoliberalismo

12xx = Terra, moradia e urbanismo
  1201=Reforma agrária, 1202=Moradia urbana, 1203=Remoções forçadas,
  1204=Transporte público, 1205=Saneamento, 1206=Megaeventos (contra)

13xx = Educação e ciência
  1301=Financiamento educação, 1302=Autonomia universitária,
  1303=Cortes em pesquisa, 1304=Passe livre estudantil, 1305=Currículo escolar

14xx = Saúde e seguridade social
  1401=Financiamento SUS, 1402=Gestão pandemia, 1403=Previdência, 1404=Medicamentos

15xx = Raça, etnia e identidade
  1501=Racismo estrutural, 1502=Cotas raciais, 1503=Violência policial racializada,
  1504=Terras indígenas, 1505=Quilombolas, 1506=Crime de ódio racial/étnico

16xx = Gênero e sexualidade
  1601=Direitos das mulheres, 1602=Violência de gênero, 1603=Direitos LGBTQIA+,
  1604=Aborto, 1605=Assédio sexual, 1606=Crime de ódio de gênero

17xx = Meio ambiente
  1701=Desmatamento, 1702=Mudanças climáticas, 1703=Licenciamento ambiental,
  1704=Energia (nuclear/hidrelétrica), 1705=Agrotóxicos, 1706=Desastre socioambiental

18xx = Segurança pública
  1801=Violência policial, 1802=Segurança pública, 1803=Milícias,
  1804=Pena de morte/maioridade penal, 1805=Armamento, 1806=Presos políticos

19xx = Política externa
  1901=Antiimperialismo, 1902=Acordos comerciais, 1903=Solidariedade, 1904=Migrantes

## VALÊNCIA
"01" = Pró-movimento / favorável à demanda
"02" = Anti-movimento / contrário à demanda
"03" = Indeterminado

## ESTIMATIVA DE MULTIDÃO
- Número exato ou "aproximadamente X" → preencher exact_count (inteiro)
- Expressões vagas ("grande multidão", "milhares") → preencher range_expression, exact_count = null

Valores possíveis de range_expression: "XS" (<50), "S" (50-499), "M" (500-4999),
"L" (5000-49999), "XL" (50000-499999), "XXL" (500000+)

## INSTRUÇÃO DE SAÍDA

Se o artigo NÃO contiver evento de protesto elegível, retorne EXATAMENTE:
{"eligible": false, "reason": "<motivo em uma frase>"}

Se contiver UM OU MAIS eventos elegíveis, retorne um array JSON com
todos os eventos, cada um no formato abaixo. Retorne SOMENTE o JSON,
sem markdown, sem explicações, sem texto antes ou depois.

FORMATO DE CADA EVENTO:
{
  "event_id": "<uuid determinístico baseado em data+cidade+ator_principal>",
  "date": "<YYYY-MM-DD>",
  "location": {
    "city": "<nome do município>",
    "state": "<sigla 2 letras>"
  },
  "actors": ["<lista de atores>"],
  "targets": ["<lista de alvos/destinatários das demandas>"],
  "claims": [
    {
      "claim_code": "<4 dígitos>",
      "valence": "<01|02|03>",
      "description": "<descrição da demanda em 1-2 frases>"
    }
  ],
  "crowd_size": {
    "exact_count": <inteiro ou null>,
    "range_expression": "<XS|S|M|L|XL|XXL ou null>"
  },
  "police_response": {
    "presence": <true|false>,
    "tactics": ["<lista de táticas se presença=true>"],
    "coercive_equipment": ["<lista de equipamentos se relatados>"]
  },
  "consequences": {
    "arrests_count": <inteiro ou null>,
    "injuries_protesters": <inteiro ou null>,
    "injuries_police": <inteiro ou null>,
    "fatalities": <inteiro ou null>,
    "property_damage": <true|false>
  },
  "_meta": {
    "source_article_id": "<id do artigo fonte>",
    "source_url": "<url do artigo>",
    "pub_date": "<data de publicação>",
    "confidence": "<high|medium|low>",
    "coder_model": "claude-sonnet-4-20250514"
  }
}"""


USER_PROMPT_TEMPLATE = """Analise o artigo abaixo e extraia todos os eventos de protesto elegíveis.

ARTIGO:
Título: {title}
Subtítulo: {subtitle}
Data: {pub_date}
Editoria: {section}
URL: {url}

TEXTO:
{body}

Retorne apenas o JSON conforme as instruções."""


# ─────────────────────────────────────────────────────────────
# Geração de UUID determinístico
# ─────────────────────────────────────────────────────────────

def deterministic_uuid(date: str, city: str, actor: str) -> str:
    """Gera UUID v5 baseado em namespace + seed determinística."""
    seed = f"{date}|{city.lower()}|{actor.lower()}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


# ─────────────────────────────────────────────────────────────
# Codificação via Claude API
# ─────────────────────────────────────────────────────────────

def code_article(article: dict) -> list[dict] | None:
    """
    Envia artigo para Claude e retorna lista de eventos codificados.
    Retorna None em caso de erro irrecuperável.
    Retorna lista vazia se artigo for inelegível.
    """
    user_msg = USER_PROMPT_TEMPLATE.format(
        title    = article.get("title", ""),
        subtitle = article.get("subtitle", ""),
        pub_date = article.get("pub_date", ""),
        section  = article.get("section", ""),
        url      = article.get("url", ""),
        body     = article.get("body", "")[:8000],  # limita a ~8k chars
    )

    for attempt in range(3):
        try:
            response = client.messages.create(
                model      = "claude-sonnet-4-20250514",
                max_tokens = 4096,
                system     = SYSTEM_PROMPT,
                messages   = [{"role": "user", "content": user_msg}],
            )
            raw = response.content[0].text.strip()

            # Remove fences de markdown se presentes
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            parsed = json.loads(raw)

            # Inelegível
            if isinstance(parsed, dict) and parsed.get("eligible") is False:
                log.debug(f"Inelegível: {parsed.get('reason', '')}")
                return []

            # Normaliza: pode retornar dict único ou array
            events = parsed if isinstance(parsed, list) else [parsed]

            # Garante IDs determinísticos e injeta metadados
            for ev in events:
                if not ev.get("event_id") or len(ev["event_id"]) < 8:
                    actor = ev.get("actors", [""])[0]
                    city  = ev.get("location", {}).get("city", "")
                    ev["event_id"] = deterministic_uuid(ev.get("date", ""), city, actor)
                if "_meta" not in ev:
                    ev["_meta"] = {}
                ev["_meta"].update({
                    "source_article_id": article.get("article_id"),
                    "source_url":        article.get("url"),
                    "pub_date":          article.get("pub_date"),
                    "coder_model":       "claude-sonnet-4-20250514",
                })

            return events

        except json.JSONDecodeError as e:
            log.warning(f"Tentativa {attempt+1}: JSON inválido — {e}")
            time.sleep(2 ** attempt)
        except anthropic.RateLimitError:
            log.warning("Rate limit atingido. Aguardando 60s...")
            time.sleep(60)
        except anthropic.APIError as e:
            log.error(f"Erro de API: {e}")
            time.sleep(5)

    log.error(f"Falha após 3 tentativas para artigo {article.get('article_id')}")
    return None


# ─────────────────────────────────────────────────────────────
# Controle de duplicatas pós-codificação
# ─────────────────────────────────────────────────────────────

def load_coded_ids() -> set:
    """Retorna conjunto de article_ids já codificados."""
    return {
        json.load(open(p))["_meta"]["source_article_id"]
        for p in CODED_DIR.glob("*.json")
        if "source_article_id" in json.load(open(p)).get("_meta", {})
    }


def save_event(event: dict) -> None:
    path = CODED_DIR / f"{event['event_id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(event, f, ensure_ascii=False, indent=2)


def save_rejected(article: dict, reason: str) -> None:
    path = REJECTED_DIR / f"{article.get('article_id', 'unknown')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"article": article, "reason": reason, "rejected_at": datetime.utcnow().isoformat()},
                  f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────
# Orquestrador
# ─────────────────────────────────────────────────────────────

def run_coder(batch_size: int = 50):
    """
    Processa todos os artigos brutos ainda não codificados.
    batch_size: número de artigos por execução (para controlar custos de API).
    """
    all_articles = sorted(RAW_DIR.glob("*.json"), key=lambda p: p.stem)
    already_coded = load_coded_ids()

    pending = [p for p in all_articles
               if json.load(open(p)).get("article_id") not in already_coded]

    log.info(f"Artigos pendentes de codificação: {len(pending)}")
    log.info(f"Processando em lotes de {batch_size}...")

    stats = {"events": 0, "ineligible": 0, "errors": 0}

    for i, article_path in enumerate(pending[:batch_size]):
        with open(article_path, encoding="utf-8") as f:
            article = json.load(f)

        log.info(f"[{i+1}/{min(batch_size, len(pending))}] Codificando: {article.get('title', '')[:70]}")

        events = code_article(article)

        if events is None:
            stats["errors"] += 1
            save_rejected(article, "API error após 3 tentativas")
            continue

        if len(events) == 0:
            stats["ineligible"] += 1
            save_rejected(article, "Inelegível DoCA")
            continue

        for ev in events:
            save_event(ev)
            stats["events"] += 1
            log.info(f"  → Evento: {ev.get('date')} | {ev.get('location', {}).get('city')} | {ev.get('actors', ['?'])[0]}")

        # Pausa entre chamadas para respeitar rate limit
        time.sleep(1.5)

    log.info("─" * 60)
    log.info(f"Codificação concluída:")
    log.info(f"  Eventos extraídos : {stats['events']}")
    log.info(f"  Artigos inelegíveis: {stats['ineligible']}")
    log.info(f"  Erros de API       : {stats['errors']}")
    log.info(f"  Total acumulado em coded_events/: {len(list(CODED_DIR.glob('*.json')))}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Codifica artigos brutos via API Claude (DoCA)")
    parser.add_argument("--batch", type=int, default=50,
                        help="Número de artigos a processar nesta execução (default: 50)")
    args = parser.parse_args()
    run_coder(batch_size=args.batch)
