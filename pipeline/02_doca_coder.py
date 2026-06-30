"""02_doca_coder.py — Codificação DoCA de artigos via API Anthropic.

Para cada artigo em pipeline/data/raw/, envia o texto ao Claude com o system
prompt DoCA + codebook e extrai eventos de protesto em JSON validado
(structured outputs). Saída: pipeline/data/coded/{hash}.json.

- UUID5 determinístico por evento (url + data do evento)
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

EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "event_date": {"type": ["string", "null"], "description": "Data do EVENTO (YYYY-MM-DD), não da publicação"},
                    "location_city": {"type": ["string", "null"]},
                    "location_state": {"type": ["string", "null"], "description": "UF, ex: SP"},
                    "actors": {"type": "array", "items": {"type": "string"}},
                    "targets": {"type": "array", "items": {"type": "string"}},
                    "claim_code": {"type": "string", "enum": sorted(CODEBOOK["claim_codes"].keys())},
                    "claim_text": {"type": "string"},
                    "repertoire": {"type": "string", "enum": CODEBOOK["repertoires"]},
                    "crowd_size_reported": {"type": ["integer", "null"]},
                    "crowd_size_scale": {"type": "string", "enum": sorted(CODEBOOK["crowd_size_scale"].keys())},
                    "police_presence": {"type": "boolean"},
                    "repression": {"type": "string", "enum": ["none", "dispersão", "prisões", "violência"]},
                    "arrests_reported": {"type": ["integer", "null"]},
                    "injuries_reported": {"type": ["integer", "null"]},
                    "eligible": {"type": "boolean", "description": "Atende ao critério DoCA: ação coletiva + espaço público + expressão contenciosa"},
                    "notes": {"type": ["string", "null"]},
                },
                "required": [
                    "event_date", "location_city", "location_state", "actors",
                    "targets", "claim_code", "claim_text", "repertoire",
                    "crowd_size_reported", "crowd_size_scale", "police_presence",
                    "repression", "arrests_reported", "injuries_reported",
                    "eligible", "notes",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": ["events"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = f"""Você é um codificador treinado em Protest Event Analysis (PEA) seguindo o \
protocolo DoCA (Dynamics of Collective Action). Sua tarefa: ler uma matéria \
jornalística da Folha de S.Paulo e extrair TODOS os eventos de protesto \
distintos nela relatados, no esquema JSON fornecido.

CRITÉRIO DE ELEGIBILIDADE (campo eligible): o evento deve combinar
(1) ação coletiva (3+ participantes), (2) ocorrência em espaço público ou
visível ao público, e (3) expressão contenciosa de uma demanda/reivindicação.
Eventos que não atendem aos três critérios devem ser registrados com
eligible=false (ex.: coletiva de imprensa, nota de repúdio, ato fechado).

REGRAS:
- Um registro por EVENTO (mesmo dia + mesma cidade + mesma ação), não por matéria.
- event_date é a data do evento; infira do texto e da data de publicação;
  use null se impossível determinar.
- claim_code: escolha o código do codebook abaixo que melhor descreve a
  demanda PRINCIPAL do evento; detalhe em claim_text.
- crowd_size_reported: número informado pela fonte (se houver intervalos ou
  disputa polícia/organizadores, registre o menor em crowd_size_reported e
  explique em notes).
- Não invente informação ausente: use null.

CODEBOOK — claim_codes:
{json.dumps(CODEBOOK["claim_codes"], ensure_ascii=False, indent=2)}

ESCALA DE MULTIDÃO:
{json.dumps(CODEBOOK["crowd_size_scale"], ensure_ascii=False, indent=2)}
"""


def deterministic_id(url: str, event_date: str | None, idx: int) -> str:
    return str(uuid.uuid5(DOCA_NAMESPACE, f"{url}|{event_date}|{idx}"))


def code_article(client: anthropic.Anthropic, art: dict) -> dict:
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
                f"{art.get('text', '')[:50000]}"
            ),
        }],
    )
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    for i, ev in enumerate(data["events"]):
        ev["event_id"] = deterministic_id(art.get("url", ""), ev.get("event_date"), i)
        ev["source_url"] = art.get("url")
        ev["source_date"] = art.get("date_hint")
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

    for path in tqdm(pending):
        art = json.loads(path.read_text())
        if not art.get("text"):
            continue
        try:
            result = code_article(client, art)
        except anthropic.APIStatusError as e:
            print(f"[erro API] {path.name}: {e.status_code} {e.message}")
            continue
        (CODED_DIR / path.name).write_text(
            json.dumps(result, ensure_ascii=False, indent=2)
        )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=None,
                    help="codifica no máximo N artigos (controle de custo)")
    run(ap.parse_args().batch)
