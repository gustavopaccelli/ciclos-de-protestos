# Tutorial: Pipeline PEA — Acervo Folha de S.Paulo

**Protocolo de busca, extração e codificação automática de eventos de protesto**
Baseado no projeto DoCA (Dynamics of Collective Action)

---

## Visão geral

Este pipeline realiza três operações em sequência:

```
Acervo Folha  →  [01_scraper]  →  Artigos brutos (JSON)
                                         ↓
                             [02_doca_coder] + Claude API
                                         ↓
                             Eventos codificados (JSON)
                                         ↓
                             [03_build_dataset]
                                         ↓
                         Dataset final (CSV + XLSX)
```

---

## Pré-requisitos

- Python 3.11 ou superior
- Assinatura ativa do Acervo Folha (folha.com.br/assine ou acesso via portal CAPES)
- Chave de API da Anthropic (console.anthropic.com)
- ~2 GB de espaço em disco para coleta de larga escala

---

## Passo 1 — Instalação do ambiente

Abra o terminal na pasta do projeto e execute:

```bash
# Cria e ativa ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Instala dependências Python
pip install -r requirements.txt

# Instala o navegador Chromium (usado pelo Playwright)
python -m playwright install chromium
```

---

## Passo 2 — Configuração das credenciais

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Abra o arquivo `.env` em qualquer editor de texto e preencha:

```
FOLHA_EMAIL=seu_email@email.com
FOLHA_PASSWORD=sua_senha
ANTHROPIC_API_KEY=sk-ant-...
START_DATE=1985-01-01
END_DATE=2024-12-31
REQUEST_DELAY=3
MAX_ARTICLES=0
```

**Importante:** o arquivo `.env` nunca deve ser compartilhado ou versionado no Git.
Se estiver usando Git, confirme que `.env` está listado no `.gitignore`.

---

## Passo 3 — Ajuste dos parâmetros de busca (opcional)

O arquivo `config/queries.yaml` controla quais termos são buscados,
quais seções do jornal são incluídas e quais são excluídas.

Para uma primeira coleta, os padrões já estão calibrados. Se quiser
restringir a um período específico ou a um conjunto de termos menor,
edite o arquivo antes de executar.

---

## Passo 4 — Execução do pipeline

### Opção A: pipeline completo (recomendado para a primeira execução)

```bash
python run_pipeline.py --step all
```

O pipeline executará as quatro etapas em sequência. Para uma coleta
de 40 anos de arquivo, espere horas ou dias dependendo da velocidade
da conexão e dos limites de requisição do acervo.

### Opção B: etapas individuais

Se quiser executar cada etapa separadamente (útil para retomar
coletas interrompidas ou para testar a codificação antes de coletar
todos os artigos):

```bash
# Apenas coleta de artigos
python run_pipeline.py --step scrape

# Apenas codificação (50 artigos por execução)
python run_pipeline.py --step code --batch 50

# Apenas consolidação do dataset
python run_pipeline.py --step build

# Apenas relatório de confiabilidade intercodificadores
python run_pipeline.py --step check
```

**Dica:** a coleta é incremental. Se for interrompida, retome com o
mesmo comando — artigos já coletados serão detectados e pulados.

---

## Passo 5 — Entendendo os arquivos gerados

Após a execução, a estrutura de pastas será:

```
output/
├── raw_articles/          ← artigos brutos do Acervo (um JSON por artigo)
├── coded_events/          ← eventos codificados pelo Claude (um JSON por evento)
├── rejected_articles/     ← artigos triados como inelegíveis
├── human_coded/           ← coloque aqui suas codificações manuais (Passo 7)
├── logs/
│   ├── scraper.log
│   ├── coder.log
│   └── build_dataset.log
└── dataset/
    ├── pea_brasil_eventos.csv      ← dataset plano, importável no R/STATA/SPSS
    ├── pea_brasil_eventos.xlsx     ← Excel com múltiplas abas analíticas
    ├── validation_report.json      ← relatório de qualidade dos dados
    └── intercoder_reliability.json ← Kappa e outras métricas de confiabilidade
```

---

## Passo 6 — Interpretando o dataset final

O arquivo `pea_brasil_eventos.xlsx` contém quatro abas:

| Aba | Conteúdo |
|-----|----------|
| `eventos` | Tabela principal: uma linha por evento de protesto |
| `por_ano` | Agregação anual: n° de eventos, repressão, prisões |
| `frequencia_claims` | Ranking dos claim codes mais frequentes |
| `distribuicao_geografica` | Eventos por estado e cidade |

### Colunas principais da aba `eventos`

| Coluna | Descrição |
|--------|-----------|
| `event_id` | UUID determinístico único por evento |
| `date` | Data do evento (YYYY-MM-DD) |
| `city` / `state` | Localização |
| `actors` | Atores mobilizadores |
| `targets` | Alvos das demandas |
| `claim_codes` | Códigos DoCA separados por "; " |
| `claims_full` | Claims completos: código:valência:descrição |
| `crowd_exact` | Tamanho exato (se relatado) |
| `crowd_range` | Faixa ordinal (XS/S/M/L/XL/XXL) |
| `police_presence` | TRUE/FALSE |
| `arrests` | Número de prisões (null se não reportado) |
| `injuries_protesters` | Manifestantes feridos |
| `fatalities` | Mortes |
| `property_damage` | Danos materiais (TRUE/FALSE) |
| `confidence` | Confiança da codificação: high/medium/low |
| `source_url` | Link para o artigo original no Acervo |

---

## Passo 7 — Validação por dupla codificação (obrigatório para publicação)

Para garantir confiabilidade acadêmica do dataset, você precisará
codificar manualmente uma amostra dos artigos e comparar com a
codificação automática.

**Procedimento:**

1. Selecione aleatoriamente 80–120 artigos da pasta `output/raw_articles/`
2. Para cada artigo, aplique o protocolo DoCA manualmente e salve
   o evento no formato JSON idêntico ao de `coded_events/`
3. Nomeie cada arquivo como `<article_id>_human.json`
4. Coloque os arquivos em `output/human_coded/`
5. Execute:

```bash
python run_pipeline.py --step check
```

O script calculará:
- **Cohen's Kappa** para claim codes (meta: κ ≥ 0.60)
- **Cohen's Kappa** para presença policial
- **% Concordância** para faixa de tamanho de multidão

Se o Kappa ficar abaixo de 0.60, revise as instruções de codificação
no `config/doca_codebook.yaml` e retreine o prompt no `02_doca_coder.py`.

---

## Passo 8 — Controle de custos da API Anthropic

A codificação via Claude consome tokens da API. Estimativa de custo:

| Volume de artigos | Tokens estimados | Custo aproximado (Sonnet 4) |
|-------------------|-----------------|------------------------------|
| 500 artigos | ~2,5 M tokens | ~US$ 3–5 |
| 5.000 artigos | ~25 M tokens | ~US$ 30–50 |
| 50.000 artigos | ~250 M tokens | ~US$ 300–500 |

**Estratégias de controle:**

- Use `--batch 50` para processar em lotes controlados
- O pipeline é idempotente: artigos já codificados nunca são enviados novamente
- Para testar o pipeline antes da coleta completa, use `MAX_ARTICLES=100` no `.env`

---

## Passo 9 — Exportação para software estatístico

### R (tidyverse)
```r
library(tidyverse)
df <- read_csv("output/dataset/pea_brasil_eventos.csv")

# Distribição temporal
df %>%
  count(year) %>%
  ggplot(aes(year, n)) +
  geom_col() +
  labs(title = "Eventos de protesto no Brasil por ano (Acervo Folha)")
```

### STATA
```stata
import delimited "output/dataset/pea_brasil_eventos.csv", clear
gen year = substr(date, 1, 4)
destring year, replace
histogram year, frequency
```

### Python (análise exploratória)
```python
import pandas as pd
df = pd.read_csv("output/dataset/pea_brasil_eventos.csv")
print(df.groupby("year")["event_id"].count())
```

---

## Perguntas frequentes

**O scraper parou no meio. Perco o progresso?**
Não. A coleta é incremental: ao reexecutar `--step scrape`, artigos
já salvos em `raw_articles/` são detectados e pulados automaticamente.

**O Acervo Folha mudou o layout. O que fazer?**
Os seletores CSS estão concentrados nas funções `extract_search_results()`
e `extract_article_content()` em `01_scraper.py`. Inspecione o HTML atual
do acervo com DevTools (F12 no navegador) e atualize os seletores.

**Quero apenas artigos de um estado específico (ex: São Paulo). Como filtrar?**
Após rodar o pipeline completo, filtre o CSV:
```python
df_sp = df[df["state"] == "SP"]
```
Ou filtre durante a coleta editando `is_eligible_candidate()` em `01_scraper.py`.

**Como citar o dataset gerado?**
Siga o padrão do BEP-Cebrap:
> [Seu nome] (ano). *Banco de Eventos de Protesto — Acervo Folha de S.Paulo
> (1985–2024)*. Protocolo DoCA. Dados não publicados / [instituição].
> Fonte primária: Folha de S.Paulo, Acervo Digital.

---

## Referências metodológicas

- McAdam, D., Tarrow, S., & Tilly, C. (2001). *Dynamics of Contention*. Cambridge.
- Tilly, C. (2008). *Contentious Performances*. Cambridge.
- Alonso, A. et al. (2024). Análise de Eventos de Protesto: decisões metodológicas
  na organização do BEP 2013–2016. *Plural*, v.31.2, p.288–323.
- Kriesi, H. et al. (1995). *New Social Movements in Western Europe*. Minnesota.
- Lombard, M. et al. (2002). Framing in Theory and Practice. *Human Communication Research*.
