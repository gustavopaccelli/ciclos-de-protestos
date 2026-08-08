"""02_doca_coder.py — Codificação DoCA/BEP de artigos via API Anthropic.

Para cada artigo em pipeline/data/raw/, envia o texto ao Claude com o system
prompt DoCA + codebook e extrai eventos de protesto em JSON validado
(structured outputs). Saída: pipeline/data/coded/{hash}.json.

- Schema COMPLETO alinhado ao `event_schema` de config/doca_codebook.yaml:
  Blocos I–V do Protocolo BEP-CEBRAP (Alonso et al. 2024) + campos MPEDS
  (Hanna 2017). Ver docs/aep-protocol-bep.md.
- UUID5 determinístico por evento: (source_url, event_date, location_city),
  conforme codebook e protocolo §4.2 — estável a reordenações do modelo.
- Prompt caching: system prompt (instruções + codebook) é estável e cacheado
- Reexecução é incremental: artigos já codificados são pulados
- Custo: ~1 chamada por artigo; use DOCA_MODEL=claude-sonnet-4-6 p/ triagem barata

Uso: python 02_doca_coder.py [--batch 100]
"""

import argparse
import json
import os
import uuid
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

BASE = Path(__file__).resolve().parent
RAW_DIR = BASE / "data" / "raw"
CODED_DIR = BASE / "data" / "coded"
CODEBOOK = yaml.safe_load((BASE / "config" / "doca_codebook.yaml").read_text())
MODEL = os.environ.get("DOCA_MODEL", "claude-opus-4-8")

DOCA_NAMESPACE = uuid.UUID("7c0e4d9a-1984-1992-2013-201520160000")

# Limite de caracteres do corpo do artigo enviado ao modelo. Truncamento é
# avisado explicitamente (antes era silencioso).
MAX_ARTICLE_CHARS = 50_000


def _nullable(*types: str) -> list[str]:
    return [*types, "null"]


# Vocabulários derivados do codebook — fonte única de verdade.
VENUE_TYPES = CODEBOOK["location_venue_types"]
ORG_TYPES = CODEBOOK["actor_org_types"]
FORMALIZATION = sorted(CODEBOOK["actor_formalization"].keys())
CITY_SIZES = sorted(CODEBOOK["city_size_classes"].keys())
CROWD_BEP = sorted(CODEBOOK["crowd_size_bep"].keys())
CROWD_SCALE = sorted(CODEBOOK["crowd_size_scale"].keys())
REPRESSION = sorted(CODEBOOK["repression_levels"].keys())
VALENCES = sorted(CODEBOOK["valences"].keys())
TARGETS = CODEBOOK["mpeds_target_categories"]
CLAIM_CODES = sorted(CODEBOOK["claim_codes"].keys())
REPERTOIRES = CODEBOOK["repertoires"]

ACTOR_SCHEMA = {
    "type": "object",
    "description": "Ator coletivo — Bloco II do protocolo BEP",
    "properties": {
        "name": {
            "type": "string",
            "description": "Sigla+nome quando disponível; senão categoria do movimento; senão 'manifestantes'",
        },
        "specification": {
            "type": _nullable("string"),
            "description": "Subgrupos ou indivíduos nomeados",
        },
        "org_type": {"type": "string", "enum": ORG_TYPES},
        "formalization": {"type": "string", "enum": FORMALIZATION},
    },
    "required": ["name", "specification", "org_type", "formalization"],
    "additionalProperties": False,
}

EVENT_PROPERTIES = {
    # ---- Bloco I — identificação ----
    "event_date": {
        "type": _nullable("string"),
        "description": "Data do EVENTO (YYYY-MM-DD), não da publicação",
    },
    "location_venue": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Todos os locais/trajetos do evento",
    },
    "location_venue_type": {
        "type": "string",
        "enum": VENUE_TYPES,
        "description": "Tipo do local principal; 'SI' se sem informação",
    },
    "location_conventional": {
        "type": _nullable("boolean"),
        "description": "Uso convencional do local (ver location_conventional no codebook)",
    },
    "location_city": {"type": _nullable("string")},
    "city_size": {"type": _nullable("string"), "enum": [*CITY_SIZES, None]},
    "location_state": {"type": _nullable("string"), "description": "UF, ex: SP"},
    "crowd_size_reported": {
        "type": _nullable("integer"),
        "description": "MAIOR valor de público informado pelas fontes (protocolo §5 Bloco I)",
    },
    "crowd_size_min": {
        "type": _nullable("integer"),
        "description": "Menor estimativa informada, quando há divergência entre fontes",
    },
    "crowd_size_max": {
        "type": _nullable("integer"),
        "description": "Maior estimativa informada; igual a crowd_size_reported",
    },
    "crowd_size_scale": {"type": "string", "enum": CROWD_SCALE},
    "crowd_size_bep": {
        "type": _nullable("string"),
        "enum": [*CROWD_BEP, None],
        "description": "Derivado de crowd_size_reported",
    },
    # ---- Bloco II — atores ----
    "actors": {"type": "array", "items": ACTOR_SCHEMA},
    # ---- Bloco III — performances ----
    "repertoire": {"type": "string", "enum": REPERTOIRES},
    "action_object": {"type": _nullable("string")},
    "action_instrument": {"type": _nullable("string")},
    "symbols": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Bandeiras, signos visuais/corporais ostentados",
    },
    # ---- Bloco IV — temas e slogans ----
    "claim_code": {"type": "string", "enum": CLAIM_CODES},
    "claim_text": {"type": "string"},
    "valence": {"type": "string", "enum": VALENCES},
    "slogans": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Slogans verbatim, grafia original",
    },
    # ---- Bloco V — respostas e interação ----
    "conflict_present": {"type": "boolean"},
    "repression": {"type": "string", "enum": REPRESSION},
    "conflict_police": {"type": "boolean"},
    "conflict_inter_group": {"type": "boolean"},
    "arrests_reported": {"type": _nullable("integer")},
    "injuries_reported": {"type": _nullable("integer")},
    # ---- Elegibilidade e notas ----
    "eligible": {
        "type": "boolean",
        "description": "Atende aos 4 critérios de evento de protesto (protocolo §2)",
    },
    "notes": {"type": _nullable("string")},
    # ---- Campos MPEDS (Hanna 2017) ----
    "end_date": {"type": _nullable("string"), "description": "YYYY-MM-DD, null se não informado"},
    "duration_days": {"type": _nullable("integer")},
    "multi_event_article": {
        "type": "boolean",
        "description": "O artigo fonte cobre múltiplos eventos de protesto?",
    },
    "article_desc": {"type": "string", "description": "Descrição do artigo, máx. 300 chars"},
    "event_desc": {"type": "string", "description": "Descrição do evento, máx. 300 chars"},
    "counter_protest": {"type": "boolean"},
    "smo": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Organizações de Movimento Social formais identificadas",
    },
    "target": {"type": "string", "enum": TARGETS, "description": "Alvo primário das reivindicações"},
}

EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": EVENT_PROPERTIES,
                "required": sorted(EVENT_PROPERTIES.keys()),
                "additionalProperties": False,
            },
        },
    },
    "required": ["events"],
    "additionalProperties": False,
}

# Campos atribuídos pelo pipeline, não pelo modelo (event_id, source_*,
# canonical_event_id). Declarados aqui para a checagem de cobertura do schema.
PIPELINE_ASSIGNED_FIELDS = {"event_id", "source_url", "source_date", "canonical_event_id"}

SYSTEM_PROMPT = f"""Você é um codificador treinado em Análise de Eventos de Protesto (AEP) \
seguindo o Protocolo BEP-CEBRAP (Alonso et al., 2024) com o esquema DoCA. Sua tarefa: ler uma \
matéria jornalística e extrair TODOS os eventos de protesto distintos nela relatados, no \
esquema JSON fornecido.

CRITÉRIO DE ELEGIBILIDADE (campo eligible) — os 4 critérios do protocolo §2:
(1) ação pública e coletiva (3+ participantes);
(2) promovida por atores não-estatais;
(3) de caráter contencioso;
(4) portadora de demanda social ou política.
Registre eligible=false quando qualquer critério falhar (ex.: coletiva de imprensa, nota de
repúdio, ato fechado, evento apenas virtual, evento anunciado mas não confirmado) e explique
em notes.

EVENTO ≠ MATÉRIA (protocolo §4):
- Um registro por EVENTO, não por matéria. Se a matéria cobre vários eventos, emita vários
  registros e marque multi_event_article=true.
- Mesmos atores em intervalo < 24h = UM evento. Ação contínua > 24h (ex.: ocupação de 5 dias)
  = UM evento (use end_date/duration_days).
- Mesmos atores com intervalo > 24h = eventos DISTINTOS.
- Mesma localidade com atores iguais ou similares, mesmo em trajetos diferentes = UM evento.
- Localidades distintas nomeadas separadamente = eventos DISTINTOS.
- Pautas opostas em trajetos sobrepostos = eventos DISTINTOS (separe por organizador).

REGRAS DE CODIFICAÇÃO:
- event_date é a data do evento; infira do texto e da data de publicação; null se impossível.
- PÚBLICO: quando houver divergência entre fontes (ex.: PM vs. organizadores) ou intervalo,
  registre o MAIOR valor em crowd_size_reported, e preserve o intervalo em crowd_size_min /
  crowd_size_max; explique a divergência em notes. Se houver um único valor, os três campos
  recebem esse valor. crowd_size_bep é derivado de crowd_size_reported.
- claim_code: o código do codebook que melhor descreve a demanda PRINCIPAL; detalhe em claim_text.
- repertoire: use o verbo/substantivo canônico; sinônimos convergem para o mais geral.
- actors: um objeto por ator coletivo. Prioridade do nome: sigla+nome > categoria do movimento >
  "manifestantes" (residual, com org_type="manifestantes").
- Não invente informação ausente: use null, listas vazias, ou "SI" onde o enum permitir.

CODEBOOK — claim_codes:
{json.dumps(CODEBOOK["claim_codes"], ensure_ascii=False, indent=2)}

REPERTÓRIOS canônicos:
{json.dumps(REPERTOIRES, ensure_ascii=False, indent=2)}

ESCALA DE MULTIDÃO (crowd_size_scale):
{json.dumps(CODEBOOK["crowd_size_scale"], ensure_ascii=False, indent=2)}

CATEGORIAS BEP DE PÚBLICO (crowd_size_bep):
{json.dumps(CODEBOOK["crowd_size_bep"], ensure_ascii=False, indent=2)}

TIPOS DE LOCAL e uso convencional:
{json.dumps(CODEBOOK["location_conventional"], ensure_ascii=False, indent=2)}

VALÊNCIAS:
{json.dumps(CODEBOOK["valences"], ensure_ascii=False, indent=2)}

NÍVEIS DE REPRESSÃO:
{json.dumps(CODEBOOK["repression_levels"], ensure_ascii=False, indent=2)}
"""


def deterministic_id(url: str, event_date: str | None, location_city: str | None) -> str:
    """UUID5 sobre (source_url, event_date, location_city) — protocolo §4.2.

    Deliberadamente NÃO usa o índice posicional do evento no artigo: o índice
    muda se o modelo reordenar a saída, o que quebraria a estabilidade do ID
    entre recodificações.
    """
    return str(uuid.uuid5(DOCA_NAMESPACE, f"{url}|{event_date}|{location_city}"))


def code_article(client: anthropic.Anthropic, art: dict) -> dict:
    body = art.get("text", "")
    if len(body) > MAX_ARTICLE_CHARS:
        print(f"[aviso] texto truncado em {MAX_ARTICLE_CHARS} chars: {art.get('url')}")
        body = body[:MAX_ARTICLE_CHARS]

    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        output_config={"format": {"type": "json_schema", "schema": EVENT_SCHEMA}},
        messages=[{
            "role": "user",
            "content": (
                f"URL: {art.get('url')}\n"
                f"Data de publicação (pista): {art.get('date_hint')}\n"
                f"Título: {art.get('title')}\n\n"
                f"{body}"
            ),
        }],
    )
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise ValueError("resposta sem bloco de texto")
    data = json.loads(text)
    for ev in data["events"]:
        ev["event_id"] = deterministic_id(
            art.get("url", ""), ev.get("event_date"), ev.get("location_city")
        )
        ev["source_url"] = art.get("url")
        ev["source_date"] = art.get("date_hint")
        # Atribuído na Passagem 4 (03_build_dataset.py), por agrupamento entre fontes.
        ev["canonical_event_id"] = None
    data["_usage"] = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_read": response.usage.cache_read_input_tokens,
    }
    return data


def run(batch: int | None) -> None:
    CODED_DIR.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()
    pending = [p for p in sorted(RAW_DIR.glob("*.json"))
               if not (CODED_DIR / p.name).exists()]
    if batch:
        pending = pending[:batch]
    print(f"{len(pending)} artigos a codificar (modelo: {MODEL})")

    falhas = 0
    for path in tqdm(pending):
        art = json.loads(path.read_text())
        if not art.get("text"):
            continue
        try:
            result = code_article(client, art)
        except anthropic.APIStatusError as e:
            print(f"[erro API] {path.name}: {e.status_code} {e.message}")
            falhas += 1
            continue
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Antes, uma resposta malformada abortava o lote inteiro.
            print(f"[erro parse] {path.name}: {type(e).__name__}: {e}")
            falhas += 1
            continue
        (CODED_DIR / path.name).write_text(
            json.dumps(result, ensure_ascii=False, indent=2)
        )
    if falhas:
        print(f"{falhas} artigo(s) falharam e permanecem pendentes para nova execução.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=None,
                    help="codifica no máximo N artigos (controle de custo)")
    run(ap.parse_args().batch)
