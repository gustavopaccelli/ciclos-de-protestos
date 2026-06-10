# Tutorial — Pipeline PEA (Acervo Folha → protest_events)

## 1. Instalação (uma vez)

```bash
cd pipeline
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env   # e preencha FOLHA_EMAIL, FOLHA_PASSWORD, ANTHROPIC_API_KEY
```

## 2. Coleta (retomável; horas a dias)

```bash
python run_pipeline.py --step scrape
```

- O estado fica em `pipeline/data/scrape_state.json`; interrompa e retome à vontade.
- Artigos brutos: `pipeline/data/raw/*.json` (1 arquivo por matéria).
- **Se coletar zero artigos**: o Acervo é uma app React e os seletores CSS mudam.
  Abra o Acervo no Chrome, `F12 → Elements`, e atualize o dicionário `SEL` no
  topo de `01_scraper.py`.

## 3. Codificação DoCA (controle de custo por lote)

```bash
python run_pipeline.py --step code --batch 100
```

- Modelo padrão: `claude-opus-4-8` (defina `DOCA_MODEL=claude-sonnet-4-6` no
  `.env` para triagem mais barata; recodifique casos difíceis com Opus depois).
- O system prompt (instruções DoCA + codebook) usa **prompt caching** — a
  partir do 2º artigo o custo de entrada cai ~90%.
- A saída usa **structured outputs** (JSON schema): todo evento sai validado
  contra o codebook (claim_code, repertório e escala de multidão são enums).
- Estimativa de custo (Opus 4.8, matéria média ~1.500 tokens): ~US$ 0,01–0,03
  por artigo com cache; um corpus de 10 mil matérias ≈ US$ 100–300.
  Com Sonnet 4.6, ~1/2 disso.
- Incremental: artigos já codificados (`pipeline/data/coded/`) são pulados.

## 4. Dataset final

```bash
python run_pipeline.py --step build
```

Gera `data/protest_events.csv` e `data/protest_events.xlsx` (4 abas:
eventos, agregação anual, frequência de claims, distribuição geográfica).

## 5. Confiabilidade intercodificadores

1. Sorteie uma amostra (~5–10% dos eventos) e codifique manualmente num CSV
   com `event_id` + as variáveis (`claim_code`, `repertoire`,
   `crowd_size_scale`, `repression`, `eligible`).
2. Rode:

```bash
python 04_intercoder_reliability.py amostra_manual.csv
```

Reporte o Kappa por variável no paper (alvo: ≥ 0,61 — "substancial").

## 6. Exportação para R/Stata

```r
df <- read.csv("data/protest_events.csv")          # R
```
```stata
import delimited "data/protest_events.csv", clear  // Stata
```

## Avisos

- `config/doca_codebook.yaml` é uma **reconstrução** do codebook original
  (o YAML da sessão anterior não está no repositório). Valide os claim codes
  antes de codificar em escala.
- Respeite os termos de uso do Acervo Folha; a coleta usa sua assinatura
  pessoal com delay de 2s entre requisições.
- Nunca commite o `.env`.
