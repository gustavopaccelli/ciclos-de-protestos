"""coder.py — Codificação AEP-BR de matérias via API Anthropic.

Para cada matéria em bancos/03_aep_br/coleta/folha_acervo/, envia o texto ao
Claude com o system prompt montado a partir do codebook AEP-BR e extrai os
eventos de protesto em JSON validado (structured outputs).
Saída: data/interim/{arquivo}.json.

- Schema GERADO de bancos/03_aep_br/codebook/codebook_aep_br.yaml (variáveis)
  e config/doca_codebook.yaml (vocabulários herdados): não há lista paralela
  de campos. Ver src/preprocessing/aep_codebook.py.
- Campos do pipeline (aep_codebook.CAMPOS_PIPELINE) não são pedidos ao modelo:
  evento_id (UUID5 determinístico), ciclo/fase (pela data), codificador,
  modelo_versao (modelo + hash do prompt, protocolo §12.6), n_fontes.
- Prompt caching: o system prompt é estável e cacheado.
- Recusa (stop_reason "refusal") é coberta pelo fallback no servidor; se a
  cadeia inteira recusar, ou a saída for cortada por max_tokens, a matéria
  fica pendente para nova execução.
- Reexecução é incremental: matérias já codificadas são puladas.

Uso: python src/preprocessing/coder.py [--batch 100]
"""

import argparse
import hashlib
import json
import os
import uuid
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
import aep_codebook as cb  # noqa: E402
from analysis.atribui_ciclo import ciclo_e_fase  # noqa: E402

import anthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

RAW_DIR = paths.FOLHA_RAW
CODED_DIR = paths.INTERIM
MODEL = os.environ.get("DOCA_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("DOCA_EFFORT", "high")

DOCA_NAMESPACE = uuid.UUID("7c0e4d9a-1984-1992-2013-201520160000")

# Limite de caracteres do corpo da matéria enviado ao modelo. Truncamento é
# avisado explicitamente.
MAX_ARTICLE_CHARS = 50_000

CAMPOS_PIPELINE = cb.CAMPOS_PIPELINE

# Campos de `fontes` que vêm dos metadados da matéria, não da leitura do modelo.
FONTE_DO_ARTIGO = {"url", "data_publicacao", "titulo"}

_TIPOS = {"date": "string", "str": "string", "int": "integer", "bool": "boolean", "enum": "string"}


def _nullable(*types: str) -> list[str]:
    return [*types, "null"]


def _enum_schema(vocab: str, nulo: bool) -> dict:
    vals = cb.valores(vocab)
    if nulo:
        return {"type": _nullable("string"), "enum": [*vals, None]}
    return {"type": "string", "enum": vals}


ACTOR_SCHEMA = {
    "type": "object",
    "description": "Ator coletivo (Bloco II do BEP)",
    "properties": {
        "name": {"type": "string",
                 "description": "Sigla+nome quando disponível; senão categoria do movimento; senão 'manifestantes'"},
        "specification": {"type": _nullable("string"), "description": "Subgrupos ou indivíduos nomeados"},
        "org_type": {"type": "string", "enum": cb.valores("actor_org_types")},
        "formalization": {"type": "string", "enum": cb.valores("actor_formalization")},
    },
    "required": ["name", "specification", "org_type", "formalization"],
    "additionalProperties": False,
}

FONTE_SCHEMA = {
    "type": "object",
    "description": "A matéria lida (uma entrada). url, data_publicacao e titulo são preenchidos pelo pipeline.",
    "properties": {
        "veiculo": {"type": "string"},
        "fonte_tipo": {"type": "string", "enum": cb.valores("fonte_tipo")},
        "papel_fonte": {"type": "string", "enum": cb.valores("papel_fonte")},
        "edicao": {"type": "string", "enum": ["impressa", "online"]},
        "secao": {"type": _nullable("string")},
        "pagina": {"type": _nullable("string")},
        "qualidade_ocr": {"type": "string", "enum": cb.valores("qualidade_ocr")},
    },
    "required": ["veiculo", "fonte_tipo", "papel_fonte", "edicao", "secao", "pagina", "qualidade_ocr"],
    "additionalProperties": False,
}

ATO_OFICIAL_SCHEMA = {
    "type": "object",
    "properties": {
        "tipo": {"type": "string", "enum": cb.valores("ato_oficial_tipo")},
        "orgao": {"type": _nullable("string")},
        "data": {"type": _nullable("string"), "description": "YYYY-MM-DD"},
        "url": {"type": _nullable("string")},
    },
    "required": ["tipo", "orgao", "data", "url"],
    "additionalProperties": False,
}

_OBJETOS = {"atores": ACTOR_SCHEMA, "fontes": FONTE_SCHEMA, "atos_oficiais": ATO_OFICIAL_SCHEMA}


def _propriedade(v: dict) -> dict:
    """Schema JSON de uma variável do codebook."""
    tipo, nulo, voc = v["tipo"], not v["obrigatoria"], v.get("vocabulario")
    if tipo == "list[obj]":
        prop = {"type": "array", "items": _OBJETOS[v["nome"]]}
    elif tipo == "list[str]":
        itens = {"type": "string"}
        if voc and cb.valores(voc) is not None:
            itens["enum"] = cb.valores(voc)
        prop = {"type": "array", "items": itens}
    elif tipo == "enum":
        prop = _enum_schema(voc, nulo)
    else:
        base = _TIPOS[tipo]
        prop = {"type": _nullable(base) if nulo else base}
    prop["description"] = v["definicao"]
    return prop


EVENT_PROPERTIES = {
    v["nome"]: _propriedade(v) for v in cb.variaveis() if v["nome"] not in CAMPOS_PIPELINE
}

EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "eventos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": EVENT_PROPERTIES,
                "required": sorted(EVENT_PROPERTIES),
                "additionalProperties": False,
            },
        },
    },
    "required": ["eventos"],
    "additionalProperties": False,
}


def _dump(obj) -> str:
    # sort_keys mantém o texto idêntico entre execuções (cache do prompt).
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)


def _monta_prompt() -> str:
    a = cb.aep()
    criterios = "\n".join(f"({i}) {c['definicao']}" for i, c in enumerate(a["criterios_elegibilidade"], 1))
    exclusoes = "\n".join(f"- {e}" for e in a["exclusoes"])
    u = a["regras_unitizacao"]
    mesmo = "\n".join(f"- {r}" for r in u["mesmo_evento"])
    distintos = "\n".join(f"- {r}" for r in u["eventos_distintos"])
    decisoes = "\n".join(f"- {k}: {' '.join(t.split())}" for k, t in a["decisoes"].items())
    vocabs = sorted({v["vocabulario"] for v in cb.variaveis()
                     if v.get("vocabulario") and v["nome"] not in CAMPOS_PIPELINE
                     and v["vocabulario"] != "actor_schema"}
                    | {"actor_org_types", "actor_formalization", "fonte_tipo", "papel_fonte",
                       "ato_oficial_tipo", "location_conventional"})
    blocos_vocab = "\n\n".join(f"{n}:\n{_dump(cb.vocab_bruto(n))}" for n in vocabs)

    return f"""Você é um codificador treinado em Análise de Eventos de Protesto (AEP) e aplica o \
codebook AEP-BR v{a['versao']}, baseado no protocolo do BEP (Alonso et al. 2024, Plural 31(2)). \
Leia uma matéria jornalística e extraia TODOS os eventos de protesto distintos nela relatados, \
no esquema JSON fornecido. Cada campo traz sua definição no esquema.

ELEGIBILIDADE (campo elegivel) — o evento precisa satisfazer os 4 critérios:
{criterios}
Exclusões:
{exclusoes}
Quando algum critério falhar, registre o evento com elegivel=false e explique em notas.

EVENTO ≠ MATÉRIA. Um registro por evento. Se a matéria relata vários eventos, emita vários \
registros e marque materia_multi_evento=true.
É o mesmo evento quando:
{mesmo}
São eventos distintos quando:
{distintos}
Ações simultâneas: {' '.join(u['acoes_simultaneas'].split())}
Dê o mesmo valor de evento_coordenado_id (um rótulo curto, ex.: "ato-nacional-2013-06-20") a \
todos os registros de um mesmo ato em várias cidades; null se não for coordenado.

PÚBLICO: {' '.join(a['regra_publico'].split())} Registre o MAIOR valor em publico_max. \
Se houver um único valor, publico_max e publico_min recebem esse valor.

DECISÕES DO CODEBOOK v{a['versao']}:
{decisoes}

CONTAGENS (detidos, feridos, mortos): null = a matéria não menciona; -1 = houve, sem número; \
inteiro ≥ 0 = número informado.

FONTES: o campo fontes recebe UMA entrada, descrevendo a matéria que você está lendo \
(veículo, tipo, papel, edição, seção, página, qualidade do OCR). Avalie qualidade_ocr pelo \
próprio texto recebido: nao_se_aplica para texto digital nativo. O campo qualidade_ocr do \
evento repete esse valor.

NÃO preencha ciclo, fase, evento_id nem codificador: o pipeline atribui esses campos.
Não invente informação ausente: use null, listas vazias ou "SI" onde o vocabulário permitir. \
Use confianca para dizer quão segura é a codificação do registro.

VOCABULÁRIOS:
{blocos_vocab}
"""


SYSTEM_PROMPT = _monta_prompt()
PROMPT_HASH = hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()[:12]


def deterministic_id(url: str, data_inicio: str | None, cidade: str | None,
                     tema_codigo: list | None, repertorio: list | None) -> str:
    """UUID5 sobre (url, data, cidade, tema principal, repertório principal).

    Não usa o índice do evento na matéria: ele muda se o modelo reordenar a
    saída. Tema e repertório entram na chave porque data+cidade não separam
    manifestação e contramanifestação relatadas na mesma matéria.
    """
    tema = (tema_codigo or [None])[0]
    rep = (repertorio or [None])[0]
    chave = f"{url}|{data_inicio}|{cidade}|{tema}|{rep}"
    return str(uuid.uuid5(DOCA_NAMESPACE, chave))


def completa_pipeline(ev: dict, art: dict, modelo: str) -> dict:
    """Preenche os campos que o pipeline, e não o modelo, é responsável por atribuir."""
    for fonte in ev.get("fontes") or []:
        fonte["url"] = art.get("url")
        fonte["data_publicacao"] = art.get("date_hint")
        fonte["titulo"] = art.get("title")
    ev["evento_id"] = deterministic_id(art.get("url", ""), ev.get("data_inicio"), ev.get("cidade"),
                                       ev.get("tema_codigo"), ev.get("repertorio"))
    ev["evento_canonico_id"] = None  # atribuído no build_dataset.py
    ev["ciclo"], ev["fase"] = (ciclo_e_fase(ev["data_inicio"]) if ev.get("data_inicio")
                               else ("fora_de_ciclo", None))
    ev["codificador"] = "llm"
    ev["modelo_versao"] = f"{modelo}#prompt:{PROMPT_HASH}"
    ev["cidade_ibge"] = None   # normalização posterior
    ev["porte_cidade"] = None  # normalização posterior (população IBGE)
    ev["n_fontes"] = len({f.get("veiculo") for f in ev.get("fontes") or []})
    return ev


class CodificacaoIncompleta(Exception):
    """Recusa da cadeia inteira ou saída cortada: a matéria fica pendente."""


def code_article(client: anthropic.Anthropic, art: dict) -> dict:
    body = art.get("text", "")
    if len(body) > MAX_ARTICLE_CHARS:
        print(f"[aviso] texto truncado em {MAX_ARTICLE_CHARS} chars: {art.get('url')}")
        body = body[:MAX_ARTICLE_CHARS]

    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=32000,
        thinking={"type": "adaptive"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": EVENT_SCHEMA}},
        messages=[{
            "role": "user",
            "content": (
                f"URL: {art.get('url')}\n"
                f"Veículo (pista): {art.get('source', 'Folha de S.Paulo')}\n"
                f"Data de publicação (pista): {art.get('date_hint')}\n"
                f"Título: {art.get('title')}\n\n"
                f"{body}"
            ),
        }],
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        cat = response.stop_details.category if response.stop_details else None
        raise CodificacaoIncompleta(f"recusa (categoria {cat})")
    if response.stop_reason == "max_tokens":
        raise CodificacaoIncompleta("saída cortada por max_tokens")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise CodificacaoIncompleta("resposta sem bloco de texto")

    data = json.loads(text)
    for ev in data["eventos"]:
        completa_pipeline(ev, art, response.model)
    data["_usage"] = {
        "modelo": response.model,
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
    print(f"{len(pending)} matérias a codificar (modelo: {MODEL}, effort: {EFFORT}, prompt: {PROMPT_HASH})")

    falhas = 0
    for path in tqdm(pending):
        art = json.loads(path.read_text())
        if not art.get("text"):
            continue
        try:
            result = code_article(client, art)
        except anthropic.RateLimitError as e:
            print(f"[limite de taxa] {path.name}: {e.message}")
            falhas += 1
            continue
        except anthropic.APIStatusError as e:
            print(f"[erro API] {path.name}: {e.status_code} {e.message}")
            falhas += 1
            continue
        except anthropic.APIConnectionError as e:
            print(f"[erro de conexão] {path.name}: {e}")
            falhas += 1
            continue
        except (CodificacaoIncompleta, json.JSONDecodeError, KeyError) as e:
            print(f"[incompleta] {path.name}: {type(e).__name__}: {e}")
            falhas += 1
            continue
        (CODED_DIR / path.name).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    if falhas:
        print(f"{falhas} matéria(s) falharam e permanecem pendentes para nova execução.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=None,
                    help="codifica no máximo N matérias (controle de custo)")
    run(ap.parse_args().batch)
