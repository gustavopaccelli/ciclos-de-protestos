# DoCA Protest Events Pipeline

## Visão Geral

Pipeline de coleta, processamento e codificação de eventos de protesto no Brasil usando o protocolo **DoCA** (Data of Contentious Action) baseado no framework BEP-CEBRAP.

**Fluxo**: Acervo Folha → Scraper → SQLite DB (DoCA schema) → Human Coding → Dataset CSV/XLSX

---

## Componentes

### 1. Scraper (`src/coleta_acervo.py`)

**Objetivo**: Coletar artigos do Acervo Folha de São Paulo usando Scrapling.

- **Entrada**: URL de busca do Acervo Folha (termo: "protesto")
- **Tecnologia**: Scrapling StealthyFetcher (simula navegador real)
- **Saída**: `data/acervo_protestos.json` (lista de artigos com título, link, data)

```bash
python src/coleta_acervo.py
```

### 2. Banco de Dados DoCA (`src/data/init_doca_database.py`)

**Objetivo**: Criar schema SQLite estruturado segundo o protocolo DoCA.

**Tabelas principais**:
- `raw_articles` — artigos brutos do scraper
- `protest_events` — eventos codificados (estrutura DoCA completa)
- `actors` — atores coletivos por evento
- `symbols_slogans` — símbolos e lemas
- `smos` — Organizações de Movimento Social
- `codebook_claims` — lookup de domínios temáticos (1xxx–9xxx)
- `codebook_repertoires` — lookup de formas de ação

```bash
python src/data/init_doca_database.py
```

### 3. Loader (`src/data/load_acervo_to_doca.py`)

**Objetivo**: Ingerir artigos do JSON na estrutura DoCA (banco de dados).

- Parseia datas em formatos variados (pt-BR)
- Gera UUIDs determinísticos para eventos
- Popula `protest_events` com placeholders (eligible=False até codificação humana)

```bash
python src/data/load_acervo_to_doca.py
```

### 4. Orquestrador Pipeline (`src/run_doca_pipeline.py`)

**Objetivo**: Executar o pipeline completo em sequência.

```bash
# Tudo: init → scrape → load
python src/run_doca_pipeline.py --step all

# Passos individuais
python src/run_doca_pipeline.py --step init
python src/run_doca_pipeline.py --step scrape
python src/run_doca_pipeline.py --step load
```

---

## Esquema DoCA

### Bloco I — Identificação do Evento

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `event_id` | UUID5 | `a1b2c3d4...` |
| `event_date` | YYYY-MM-DD | `2013-06-17` |
| `location_city` | string | `São Paulo` |
| `location_state` | string | `SP` |
| `location_venue_type` | enum | `praça-via-pública`, `órgão-poder-público` |
| `crowd_size_reported` | integer | `1500000` |
| `crowd_size_bep` | enum | `mega` (>100k), `grande` (10k–100k), `media` (2k–10k), `pequena` (<2k) |

### Bloco II — Atores Coletivos

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `actors` (relação) | list | `[{name: "CUT", org_type: "sindicato", ...}]` |

### Bloco III — Performances Políticas

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `repertoire` | enum | `marchar`, `bloquear`, `ocupar`, `greve`, `concentrar` |
| `action_object` | string | `porta de banco`, `via pública` |
| `symbols` | list | `["bandeira PT", "cartazes"]` |

### Bloco IV — Temas e Slogans

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `claim_code` | string (4 dig) | `1100` = Democratização / eleições diretas |
| `claim_text` | string | `"Diretas Já!"` |
| `valence` | enum | `01` (pró), `02` (anti), `03` (indeterminado) |

**Domínios claim_code**:
- `1xxx` — Político-institucional
- `2xxx` — Anticorrupção / ética
- `3xxx` — Direitos sociais e serviços públicos
- `4xxx` — Trabalho e economia
- `5xxx` — Terra e meio rural
- `6xxx` — Identidades e direitos civis
- `7xxx` — Meio ambiente
- `8xxx` — Pautas conservadoras / direita
- `9xxx` — Outros / solidariedade

### Bloco V — Repressão e Interação

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `conflict_present` | boolean | `true` |
| `repression` | enum | `none`, `dispersão`, `prisões`, `violência` |
| `arrests_reported` | integer | `42` |

---

## Workflow Recomendado

### Fase 1: Coleta e Preparação

```bash
# 1. Inicializar banco
python src/data/init_doca_database.py

# 2. Raspar Acervo Folha
python src/coleta_acervo.py
# Saída: data/acervo_protestos.json (raw articles)

# 3. Ingerir em banco (DoCA preliminar)
python src/data/load_acervo_to_doca.py
# Insere em protest_events com eligible=False
```

Neste ponto, você tem:
- `data/protest_events.db` — banco SQLite com eventos preliminares
- Cada evento tem `eligible=False` até codificação humana

### Fase 2: Codificação Humana (DoCA)

Após este pipeline, você deve:

1. **Revisar eventos preliminares** em `protest_events.db`
   ```sql
   SELECT event_id, event_date, location_city, article_desc 
   FROM protest_events 
   WHERE eligible = False
   ORDER BY event_date DESC;
   ```

2. **Usar ferramenta de codificação** (ex: UI de revisão, ou atualizar diretamente)
   - Atribuir `claim_code` correto (1100–9900)
   - Atribuir `repertoire` (marchar, ocupar, etc.)
   - Preencher `crowd_size_reported`, `actors`, etc.
   - Marcar `eligible = True` após revisar

3. **Aferição de confiabilidade** (Cohen's Kappa ≥ 0.75):
   ```bash
   python src/analysis/run_pipeline.py --step kappa --manual amostra_codificada.csv
   ```

### Fase 3: Dataset Final

```bash
python src/analysis/run_pipeline.py --step build
# Saída:
#   - data/protest_events_raw.csv   (uma linha por artigo-fonte)
#   - data/protest_events.csv       (uma linha por evento canônico)
#   - data/protest_events.xlsx      (análise + agregações)
```

---

## Configuração (.env)

O scraper Playwright respeita `.env` para credenciais:

```env
FOLHA_EMAIL=seu_email@example.com
FOLHA_PASSWORD=sua_senha
START_DATE=1985-01-01
END_DATE=2024-12-31
REQUEST_DELAY=3
MAX_ARTICLES=0  # 0 = unlimited
OUTPUT_DIR=output
DEBUG=false
```

---

## Verificação Rápida

```bash
# Ver estrutura do banco
sqlite3 data/protest_events.db ".schema"

# Contar eventos carregados
sqlite3 data/protest_events.db "SELECT COUNT(*) FROM protest_events;"

# Listar primeiros eventos
sqlite3 data/protest_events.db "SELECT event_date, location_city, claim_code FROM protest_events LIMIT 5;"
```

---

## Referências

- **DoCA Codebook**: `config/doca_codebook.yaml`
- **Protocolo BEP-CEBRAP**: `docs/aep-protocol-bep.md`
- **MPEDS Taxonomy**: Hanna (2017) — `config/doca_codebook.yaml` (secção `mpeds_*`)

---

## Status Atual

- ✅ Scraper (Scrapling): implementado
- ✅ Banco de dados (DoCA schema): inicializado
- ✅ Loader: aguardando dados do scraper
- ⏳ Codificação humana: aguardando interface
- ⏳ Dataset final: disponível após codificação

