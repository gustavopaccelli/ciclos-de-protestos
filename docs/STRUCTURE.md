# Estrutura de Dados - Ciclos de Protesto Brasil (1985-2024)

**Última atualização**: 2026-09-21  
**Versão**: 1.0  
**Responsável**: Gustavo Paccelli

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Bases Empíricas](#bases-empíricas)
5. [Padrões de Nomeação](#padrões-de-nomeação)
6. [Metadados e Proveniência](#metadados-e-proveniência)
7. [Instruções de Uso](#instruções-de-uso)
8. [Operações Comuns](#operações-comuns)

---

## Visão Geral

A pasta `data/` armazena todas as bases de dados empíricas do projeto, organizadas segundo o padrão **Cookiecutter Data Science** adaptado para este projeto de pesquisa.

### Princípios Organizacionais

| Princípio | Implementação |
|-----------|---------------|
| **Reprodutibilidade** | Metadados JSON documentam proveniência, versão e datas |
| **Rastreabilidade** | Histórico Git preservado via `git mv`; nenhum arquivo deletado sem documentação |
| **Escalabilidade** | Estrutura pronta para novos ciclos e bases (ex: Acervo Folha) |
| **Segurança** | Dados volumosos ignorados pelo `.gitignore`; apenas metadatas no Git |
| **Clareza** | READMEs em cada nível; variáveis documentadas em `docs/codebook.md` |

---

## Estrutura de Diretórios

### 🔴 data/raw/ - Dados Brutos (Não Modificados)

Armazena dados originais de cada fonte **exatamente como recebidos**, sem processamento.

```
data/raw/
├── nepac/                          Base NEPAC/UNICAMP (2011-2016)
│   ├── .gitkeep
│   ├── metadata_nepac.json         [RASTREADO] Proveniência
│   ├── README.md
│   ├── dados/
│   │   └── protestos_2011-2016.csv
│   ├── fonte-original/
│   │   ├── protestos_no_brasil_2011-2016.xlsx
│   │   └── tatagiba_galvao_2019_livro_de_codigo.docx
│   └── livro-codigo/
│       └── livro-de-codigo.md
│
├── mass_mobilization/              Base Mass Mobilization (1990-2020)
│   ├── .gitkeep
│   ├── metadata_mm.json            [RASTREADO] Proveniência
│   ├── README.md
│   ├── dados/
│   │   └── protestos_brasil_1990-2020.csv
│   ├── fonte-original/
│   │   └── MM_users_manual_0515.pdf
│   └── livro-codigo/
│       ├── livro-de-codigo.md
│       └── crosswalk-codigos.md
│
├── seeds_historicas/               Sementes Históricas (Diretas Já + Fora Collor)
│   ├── .gitkeep
│   ├── metadata_seeds.json         [RASTREADO] Proveniência
│   ├── README.md
│   ├── diretas_ja/
│   │   ├── README.md
│   │   ├── comicios_por_estado.csv
│   │   ├── comicios_cronologia.csv
│   │   ├── grupos_associacoes.csv
│   │   └── protest_events_diretas_ja_seed.csv
│   └── fora_collor/
│       └── protest_events_fora_collor_seed.csv
│
└── folha_acervo/                   Acervo Folha de S.Paulo (Future)
    ├── .gitkeep
    └── metadata_folha.json         [RASTREADO] Status: Aguardando credenciais

**Política de Rastreamento (.gitignore)**
- ✅ Permite: .gitkeep, metadata*.json, README.md, *.md (documentação)
- ❌ Bloqueia: *.csv, *.xlsx, *.parquet, *.zip (dados volumosos)
```

#### Informações por Base

**1. NEPAC/UNICAMP (data/raw/nepac/)**
- **Período coberto**: 2011-2016
- **Número de eventos**: 9.947
- **Responsáveis originais**: Luciana Tatagiba, Andreia Galvão, Thiago Trindade (UNICAMP)
- **Referência**: Tatagiba et al. (2019) - IPEA
- **Variáveis principais**: data, localização, tipo_evento, atores, reivindicações, violência, repressão
- **Licença**: Sob permissão - consultar originais
- **Ciclos cobertos**: Junho 2013 (2011-2014), Impeachment Dilma (2015-2016)

**2. Mass Mobilization Project (data/raw/mass_mobilization/)**
- **Período coberto**: 1990-2020 (global), Brasil específico também
- **Número de eventos (Brasil)**: 3.487
- **Responsáveis**: David E. Clark (University of Michigan), Patrick M. Regan (University of Notre Dame)
- **Fonte**: Harvard Dataverse (v16, 2020)
- **Variáveis principais**: data, localização, tipo_evento, tamanho_estimado, fonte
- **Licença**: Domínio público
- **Ciclos cobertos**: Todos (1990-2020 como triangulação)

**3. Sementes Históricas (data/raw/seeds_historicas/)**
- **Período coberto**: 1983-1993
- **Número de registros**: ~401 (Diretas Já: 245, Fora Collor: 156)
- **Responsável**: Gustavo Paccelli (coleta manual)
- **Origem**: Literatura secundária, cronologias, Acervo Folha digitalizados
- **Status**: Validação pendente de especialistas
- **Ciclos cobertos**: Diretas Já (1983-1985), Fora Collor (1991-1993)

**4. Acervo Folha (data/raw/folha_acervo/)**
- **Período alvo**: 1985-2024
- **Status**: Aguardando credenciais de acesso + desenvolvimento de scraper
- **Protocolo ética**: BEP-CEBRAP (aprovado)
- **Fonte**: https://acervo.folha.com.br/
- **Variáveis esperadas**: data_publicação, título, seção, descrição_evento, localização, atores, reivindicações, tamanho_estimado
- **Próximas ações**: Obter credenciais, desenvolver scraper, coleta piloto 2011-2016, expansão 1985-2010

---

### 🟡 data/interim/ - Dados em Processamento

Armazena versões **parcialmente processadas** de dados brutos, em caminho para versão final.

```
data/interim/
├── .gitkeep
├── README.md                       Documentação do fluxo
├── nepac/                          NEPAC após limpeza e padronização
│   └── .gitkeep
├── mass_mobilization/              Mass Mobilization após limpeza e harmonização
│   └── .gitkeep
└── seeds/                          Seeds após validação preliminar
    └── .gitkeep

**Operações Típicas**
- Remover duplicatas
- Normalizar nomes de cidades/estados
- Validar datas e localizações
- Converter formatos (XLSX → CSV)
- Marcar registros problemáticos
```

#### Saídas Esperadas

Cada subpasta (nepac/, mass_mobilization/, seeds/) deve conter após processamento:

```
data/interim/{base}/
├── dados_processados.csv           Dados limpos
├── log_limpeza.txt                 O que foi removido/modificado
├── dicionário_local.md             Variações de código locais (se houver)
└── problemas.csv                   Registros que precisam revisão manual
```

---

### 🟢 data/processed/ - Dados Finais Processados

Armazena versões **finais, harmonizadas e validadas**, prontas para análise.

```
data/processed/
├── .gitkeep
├── README.md                       Documentação
├── harmonizado/                    Base canônica unificada
│   └── .gitkeep
│       (Future: protestos_brasil_1985-2024_harmonizado.csv)
│       (Future: log_triangulacao.json)
└── cycle_phases/                   Fases de ciclos de protesto
    ├── .gitkeep
    ├── cycle_phases.csv            Datas de fases por ciclo
    └── cycle_phases_v2_prearticulacao.csv
```

#### Saídas Esperadas

**harmonizado/**
```
protestos_brasil_1985-2024_harmonizado.csv
├── event_id                    ID único harmonizado
├── data_evento                 Data padronizada
├── localização_padronizada     Cidade, estado, região
├── tipo_evento                 Categoria unificada
├── tamanho_estimado            Escala padronizada
├── atores                      Parsed e codificado
├── reivindicações              Parsed e codificado
├── fontes_originais            Referência cruzada (NEPAC/MM/seed)
├── confiabilidade              Nível de confiança do registro
└── notas_triangulacao          Como conflitos foram resolvidos
```

**cycle_phases/**
- `cycle_phases.csv`: Fases (pré-articulação, articulação, auge, desarticulação) com datas
- `cycle_phases_v2_prearticulacao.csv`: Versão expandida com fase pré-articulação mais detalhada

---

### 🔵 data/triangulacao/ - Análises de Validação Cruzada

Armazena outputs de **triangulação entre bases**, resolução de conflitos e agregações.

```
data/triangulacao/
├── .gitkeep
├── README.md                       Documentação da triangulação
├── series_temporais/               Séries temporais agregadas
│   ├── .gitkeep
│   └── series_temporais_eventos.csv Contagens mensais/semanais por ciclo
└── discrepancias/                  Eventos com conflitos entre bases
    └── .gitkeep
```

#### Saídas Esperadas

**series_temporais/**
```
series_temporais_eventos.csv
├── periodo (YYYY-MM ou YYYY-WW)
├── ciclo_id                    Qual ciclo
├── n_eventos_nepac             Contagem NEPAC nesse período
├── n_eventos_mm                Contagem Mass Mobilization
├── n_eventos_seeds             Contagem Seeds
├── n_harmonizado               Contagem final (após dedup)
├── taxa_cobertura              % de overlaps entre bases
└── notas                       Observações sobre divergências
```

**discrepancias/**
```
discrepancias_triangulacao.csv
├── event_id_nepac
├── event_id_mm
├── event_id_seed
├── data_nepac, data_mm, data_seed       Datas registradas
├── localização_nepac, localização_mm    Localizações
├── tipo_discrepância                    Qual tipo de conflito
├── resolução                            Como foi resolvido
├── fonte_privilegiada                   Qual base foi priorizada
└── confiabilidade_final                 Nível de confiança pós-resolução
```

---

## Fluxo de Dados

### Visão Geral do Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLUXO DE DADOS                            │
└─────────────────────────────────────────────────────────────────┘

COLETA (data/raw/)
    ├─ NEPAC/UNICAMP (2011-2016)
    ├─ Mass Mobilization (1990-2020)
    ├─ Sementes Históricas (1983-1993)
    └─ Acervo Folha (future)
         │
         ↓ [src/data/] - Scripts de extração/coleta
         │
PROCESSAMENTO (data/interim/)
    ├─ NEPAC → limpeza, padronização
    ├─ Mass Mobilization → filtro Brasil, harmonização
    ├─ Seeds → validação de datas/locais
    └─ Acervo Folha → (future integration)
         │
         ↓ [src/preprocessing/] - Scripts de validação
         │
TRIANGULAÇÃO (data/triangulacao/)
    ├─ Validação cruzada entre bases
    ├─ Identificação de duplicatas
    ├─ Resolução de conflitos (datas, localizações)
    └─ Séries temporais agregadas
         │
         ↓ [src/analysis/] - Scripts de harmonização
         │
SAÍDA FINAL (data/processed/)
    ├─ harmonizado/       Base canônica unificada
    └─ cycle_phases/      Fases de ciclos definidas
         │
         ↓ [outputs/]
         │
    ├─ figures/          Visualizações (gráficos, mapas)
    └─ tables/           Tabelas para artigo/relatórios
```

### Descrição de Cada Etapa

#### 1️⃣ COLETA (data/raw/)

**Objetivo**: Armazenar dados originais sem modificações

**Scripts relevantes**:
- `src/data/scraper.py` - Web scraping para Acervo Folha
- `src/data/check_schema_coverage.py` - Validar conformidade de schemas

**Outputs**:
- CSVs, XLSX, PDFs de fontes originais
- Metadados JSON documentando proveniência

**Responsabilidade**: Garantir que dados originais sempre estejam recuperáveis

---

#### 2️⃣ PROCESSAMENTO (data/interim/)

**Objetivo**: Preparar dados brutos para triangulação

**Scripts relevantes**:
- `src/preprocessing/build_dataset.py` - Construir datasets limpos
- `src/preprocessing/valida_cycle_phases.py` - Validar datas de eventos
- `src/preprocessing/pt_valida_registro.py` - Validar registros individuais

**Transformações típicas**:
```python
# Limpeza
- Remover duplicatas exatas
- Normalizar nomes de cidades (São Paulo → SP, etc)
- Validar datas (não-futuras, não-impossíveis)
- Normalizar categorias

# Padronização
- Converter datas para ISO 8601 (YYYY-MM-DD)
- Codificar atores em categorias controladas
- Normalizar reivindicações (stemming, limpeza de pontuação)

# Validação
- Verificar campos obrigatórios
- Alertar sobre valores fora de range
- Marcar registros incompletos para revisão manual
```

**Outputs**:
- CSVs limpos por base
- Logs de transformação (quantas linhas removidas, etc)
- Flags de problemas pendentes

---

#### 3️⃣ TRIANGULAÇÃO (data/triangulacao/)

**Objetivo**: Validar cruzadamente entre bases e criar versão canônica

**Scripts relevantes**:
- `src/preprocessing/intercoder_reliability.py` - Validar concordância entre bases
- `src/analysis/build_series_temporais.py` - Agregar em séries temporais

**Operações típicas**:
```
1. Deduplicação: Qual evento é o "mesmo" entre NEPAC, MM e seeds?
   - Comparar datas (tolerância: ±1 dia)
   - Comparar localizações (janela de distância)
   - Comparar descrições (similarity score)

2. Resolução de conflitos:
   - Se datas divergem: qual fonte é mais confiável?
   - Se localizações divergem: qual é mais específica?
   - Se tamanhos divergem: qual é mais plausível?

3. Agregação:
   - Contar eventos por mês/semana/estado
   - Calcular tendências por ciclo
   - Comparar cobertura entre bases por período
```

**Outputs**:
- Matriz de triangulação (qual evento em qual base)
- Log de discrepâncias resolvidas
- Séries temporais consolidadas

---

#### 4️⃣ HARMONIZAÇÃO (data/processed/)

**Objetivo**: Produzir base canônica final para análises

**Scripts relevantes**:
- `src/analysis/run_pipeline.py` - Pipeline completo

**Operações finais**:
```
1. Criação de ID único harmonizado
   - event_id_final = hash(data + localização + tipo_evento)
   - Referência cruzada com IDs originais (nepac_id, mm_id, seed_id)

2. Seleção de "versão melhor"
   - Se múltiplas fontes cobrem mesmo evento:
     → Usar data mais confiável
     → Usar descrição mais completa
     → Priorizar fonte primária (jornal > base secundária)

3. Enriquecimento final
   - Adicionar classificação de ciclo (1-4)
   - Calcular fase_ciclo (articulação, auge, desarticulação)
   - Adicionar score de confiabilidade
   - Adicionar tags (violência?, repressão?, etc)
```

**Outputs**:
- `protestos_brasil_1985-2024_harmonizado.csv` - Base canônica
- `cycle_phases.csv` - Delimitações de fases

---

## Bases Empíricas

### Mapeamento de Ciclos de Protesto

| Ciclo | Período | Bases Cobrindo | Status |
|-------|---------|-----------------|--------|
| **Diretas Já** | 1983-1985 | Seeds | ✅ Coletado |
| **Fora Collor** | 1991-1993 | Seeds | ✅ Coletado |
| **Junho 2013** | 2011-2014 | NEPAC, MM, Seeds | ✅ Coletado (3 fontes) |
| **Impeachment Dilma** | 2014-2016 | NEPAC, MM | ✅ Coletado (2 fontes) |
| **Pós-2016** | 2016-2024 | MM (parcial) | ⏳ Incompleto (Acervo Folha future) |

### Cobertura Temporal por Base

```
1980 ─────|──────────────────────────────────────────────────────── 2024
          │
Diretas   │      Fora      Junho              Dilma
Já        │    Collor      2013             Impeachment
1983-85   │    1991-93     2011-14           2014-16
          │
Seeds     ├──────┤            MM Coverage ├────────────────────────────┤
          │                                                           │
          │                  NEPAC Coverage ├──────────┤
          │                                 2011      2016
          │
          │                                 Folha Acervo (future)
          │                                 ├────────────────────────────────────┤
          │                                 1985                              2024
          │
          └──────────────────────────────────────────────────────────────────────┘
```

### Comparação de Bases

| Aspecto | NEPAC | MM | Seeds | Folha |
|---------|-------|----|----|-------|
| **Período** | 2011-16 | 1990-20 | 1983-93 | 1985-24 |
| **Eventos (Brasil)** | 9.947 | 3.487 | ~401 | TBD |
| **Granularidade** | Evento individual | Agregado | Evento seed | Individual |
| **Fonte primária** | Bases jornalísticas | Compilação acadêmica | Literatura + jornal | Jornal original |
| **Detalhamento** | Alto (20+ variáveis) | Médio (8+ variáveis) | Básico (5-8 var) | Alto (esperado) |
| **Viés geográfico** | Relativo (cobertura nacional) | Alto (capitais) | Alto (SP) | Alto (SP) |

---

## Padrões de Nomeação

### Convenções para Arquivos

```
data/{nivel}/{base}/{tipo}/
    └─ {descricao}_{versao}.{ext}

Exemplos:
- data/raw/nepac/dados/protestos_2011-2016.csv
- data/interim/nepac/nepac_limpo_v1.csv
- data/processed/harmonizado/protestos_brasil_harmonizado_v2.csv
- data/triangulacao/discrepancias/discrepancias_triangulacao_v1.csv
```

### Variáveis Padronizadas

Todas as bases devem usar estas variáveis quando aplicável (cf. `docs/codebook.md`):

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `event_id` | String | ID único do evento |
| `data_evento` | Date (YYYY-MM-DD) | Data do evento |
| `localização_principal` | String | Descrição da localização |
| `estado` | String (sigla) | UF (SP, RJ, MG, etc) |
| `municipio` | String | Município |
| `tipo_evento` | Categorical | manifestacao, passeata, bloqueio, ocupacao, etc |
| `tamanho_estimado` | Categorical | pequeno, médio, grande, muito_grande, desconhecido |
| `atores_principais` | Categorical (multi) | sindicatos, estudantes, igrejas, etc |
| `reivindicações_principais` | Text | Demandas descritas |
| `violência` | Boolean | Houve confronto/violência? |
| `prisões` | Integer | Número de prisões (ou -1 se desconhecido) |
| `fonte_primária` | Categorical | jornal, documento_oficial, testemunha, etc |
| `ciclo_id` | Categorical | diretas_ja, fora_collor, junho_2013, dilma_impeachment |

---

## Metadados e Proveniência

### Arquivos metadata*.json

Cada base em `data/raw/` possui um arquivo `metadata*.json` documentando:

```json
{
  "nome_base": "Nome completo da base",
  "responsáveis": ["Autor 1", "Autor 2"],
  "url_fonte": "https://...",
  "versão": "v1.0 ou data",
  "data_coleta_original": "YYYY-MM-DD",
  "data_integração_repositório": "YYYY-MM-DD",
  "descrição": "Descrição breve",
  "cobertura_temporal": {
    "início": "YYYY-MM-DD",
    "fim": "YYYY-MM-DD"
  },
  "cobertura_geográfica": "Brasil (descrição)",
  "número_eventos": 9947,
  "variáveis_principais": ["lista", "de", "variáveis"],
  "formato_dados": "CSV, XLSX, JSON, etc",
  "arquivos": {
    "dados_brutos": "nome.csv",
    "documentação": "livro-de-codigo.md"
  },
  "licença": "Descrição de licença",
  "notas_integração": "Como foi integrada",
  "contato": "responsavel@email.com",
  "última_atualização": "YYYY-MM-DD"
}
```

**Exemplo** (NEPAC):
```json
{
  "nome_base": "NEPAC/UNICAMP - Banco de Dados de Protestos (2011-2016)",
  "responsáveis": ["Luciana Tatagiba", "Andreia Galvão", "Thiago Trindade"],
  "url_fonte": "https://www.ifch.unicamp.br/nepp/",
  "versão": "Original (2019)",
  "data_coleta_original": "2011-2016",
  "número_eventos": 9947,
  "licença": "Sob permissão - consultar originais"
}
```

### READMEs por Nível

- `data/interim/README.md` - Explica o fluxo de limpeza
- `data/processed/README.md` - Explica harmonizado/ e cycle_phases/
- `data/triangulacao/README.md` - Explica triangulação e discrepâncias
- `docs/codebook.md` - Dicionário completo de variáveis

---

## Instruções de Uso

### Para Pesquisadores

#### ✅ FAÇA

```bash
# 1. Explorar dados
less data/raw/nepac/metadata_nepac.json    # Ver proveniência
cat data/raw/nepac/README.md               # Ver estrutura

# 2. Usar dados processados
python -c "import pandas as pd; df = pd.read_csv('data/processed/harmonizado/protestos_brasil_harmonizado.csv')"

# 3. Revisar qualidade
cat data/triangulacao/README.md            # Entender triangulação
cat data/triangulacao/discrepancias/discrepancias_triangulacao.csv  # Ver conflitos

# 4. Citar proveniência
# Ver docs/codebook.md + metadata JSON antes de publicar
```

#### ❌ NÃO FAÇA

```bash
# ❌ Nunca modificar data/raw/ diretamente
rm data/raw/nepac/dados/protestos_2011-2016.csv   # ERRO!

# ❌ Nunca criar novas versões sem documentação
cp data/processed/harmonizado/protestos.csv data/protestos_v2.csv  # ERRO!

# ❌ Nunca ignorar metadados
# Sempre consultar metadata*.json antes de usar base

# ❌ Nunca fazer commit de dados volumosos
git add data/raw/nepac/dados/protestos_2011-2016.csv  # BLOQUEADO pelo .gitignore
```

---

### Para Desenvolvedores (Scripts de Processamento)

#### Leitura de Dados Brutos

```python
# src/preprocessing/build_dataset.py

import pandas as pd
import json

# 1. Ler metadados
with open('data/raw/nepac/metadata_nepac.json') as f:
    meta = json.load(f)
    print(f"Base: {meta['nome_base']}")
    print(f"Período: {meta['cobertura_temporal']}")

# 2. Ler dados brutos
df_nepac = pd.read_csv('data/raw/nepac/dados/protestos_2011-2016.csv')
print(f"Eventos NEPAC: {len(df_nepac)}")

# 3. Aplicar transformações
df_nepac['data_evento'] = pd.to_datetime(df_nepac['data_evento'])
df_nepac = df_nepac.drop_duplicates()

# 4. Salvar em interim
df_nepac.to_csv('data/interim/nepac/nepac_limpo_v1.csv', index=False)
print("Salvo em data/interim/nepac/")
```

#### Triangulação

```python
# src/analysis/build_series_temporais.py

import pandas as pd

# Carregar bases processadas
df_nepac = pd.read_csv('data/interim/nepac/nepac_limpo_v1.csv')
df_mm = pd.read_csv('data/interim/mass_mobilization/mm_limpo_v1.csv')
df_seeds = pd.read_csv('data/interim/seeds/seeds_limpo_v1.csv')

# Triangular: encontrar duplicatas entre bases
# (lógica de matching: data ± 1 dia, local similar, tipo similar)

# Agregar em séries temporais
series = df_final.groupby(pd.Grouper(key='data_evento', freq='MS')).size()
series.to_csv('data/triangulacao/series_temporais/series_mensais.csv')
```

#### Escrita em Processed

```python
# src/analysis/run_pipeline.py

# Após triangulação, salvar versão final harmonizada
df_harmonizado.to_csv(
    'data/processed/harmonizado/protestos_brasil_1985-2024_harmonizado.csv',
    index=False,
    encoding='utf-8'
)

# Incluir metadados de rastreabilidade
metadata_final = {
    "data_processamento": "2026-09-21",
    "script_gerador": "src/analysis/run_pipeline.py",
    "bases_trianguladas": ["nepac", "mass_mobilization", "seeds"],
    "número_eventos_final": len(df_harmonizado),
    "versão": "v1.0"
}

import json
with open('data/processed/harmonizado/metadata_processado.json', 'w') as f:
    json.dump(metadata_final, f, indent=2)
```

---

## Operações Comuns

### 🔍 Explorar uma Base

```bash
# 1. Ver metadados
cat data/raw/nepac/metadata_nepac.json | jq '.'

# 2. Ver estrutura de arquivos
ls -lh data/raw/nepac/

# 3. Ver primeiras linhas de dados
head -5 data/raw/nepac/dados/protestos_2011-2016.csv

# 4. Ver documentação
cat data/raw/nepac/livro-codigo/livro-de-codigo.md

# 5. Ver números básicos (com Python)
python -c "import pandas as pd; df = pd.read_csv('data/raw/nepac/dados/protestos_2011-2016.csv'); print(f'Linhas: {len(df)}, Colunas: {len(df.columns)}')"
```

### 🔄 Adicionar Nova Base Futura

```bash
# 1. Criar estrutura
mkdir -p data/raw/{nova_base}/{dados,fonte-original,livro-codigo}
touch data/raw/{nova_base}/.gitkeep
touch data/raw/{nova_base}/{dados,fonte-original,livro-codigo}/.gitkeep

# 2. Criar metadados
cat > data/raw/{nova_base}/metadata_{nova_base}.json << 'EOF'
{
  "nome_base": "...",
  "responsáveis": [...],
  "url_fonte": "...",
  ...
}
EOF

# 3. Copiar dados (não fazer commit se > 100MB)
cp dados_originais.csv data/raw/{nova_base}/dados/

# 4. Criar README
cat > data/raw/{nova_base}/README.md << 'EOF'
# Nova Base
...
EOF

# 5. Commit
git add data/raw/{nova_base}/
git commit -m "feat: integração de nova base {nova_base}"
```

### 📊 Gerar Relatório de Qualidade

```bash
# Contar eventos por base
echo "=== COBERTURA POR BASE ==="
echo "NEPAC: $(wc -l < data/raw/nepac/dados/protestos_2011-2016.csv) eventos"
echo "MM: $(wc -l < data/raw/mass_mobilization/dados/protestos_brasil_1990-2020.csv) eventos"
echo "Seeds: $(wc -l < data/raw/seeds_historicas/*/protest*.csv | tail -1 | awk '{print $1}') eventos"

# Revisar discrepâncias
echo "=== DISCREPÂNCIAS TRIANGULACAO ==="
head -20 data/triangulacao/discrepancias/discrepancias_triangulacao.csv
```

### 🔗 Rastrear Evento entre Bases

```python
# Qual evento em qual base?
import pandas as pd

# Carregar dicionário de mapeo
mapping = pd.read_csv('data/triangulacao/discrepancias/eventos_mapeados.csv')

# Buscar evento específico
event = mapping[mapping['event_id_final'] == 'diretas_ja_19840421_sao_paulo_001']
print(f"NEPAC ID: {event['event_id_nepac'].values}")
print(f"MM ID: {event['event_id_mm'].values}")
print(f"Seeds ID: {event['event_id_seed'].values}")
print(f"Resolvido como: {event['resolução'].values}")
```

---

## Referências

- **Documentação de variáveis**: `docs/codebook.md`
- **Metodologia da pesquisa**: `docs/methodology.md`
- **Scripts de processamento**: `src/data/`, `src/preprocessing/`, `src/analysis/`
- **Configuração de pipeline**: `config/`
- **Ambiente**: `.env.example` → copiar para `.env` e preencher

---

## Perguntas Frequentes

### P: Onde fico os dados volumosos (CSVs, XLSXs)?
**R**: Em `data/raw/`, `data/interim/` e `data/processed/`. Não são rastreados pelo Git (`.gitignore`). Para compartilhar: use Google Drive, OSF.io, ou Zenodo.

### P: Como cito as bases neste repositório?
**R**: Consulte metadados JSON em `data/raw/*/metadata*.json`. Exemplo:
```bibtex
@dataset{nepac_tatagiba_2019,
  title={NEPAC: Banco de Dados de Protestos (2011-2016)},
  author={Tatagiba, Luciana and Galvão, Andreia and Trindade, Thiago},
  institution={UNICAMP},
  year={2019},
  url={https://www.ifch.unicamp.br/nepp/}
}
```

### P: Posso deletar arquivos em data/raw/?
**R**: Não sem documentação explícita. Se um arquivo está obsoleto, crie uma issue descrevendo por quê. Histórico é preservado via Git.

### P: Como atualizar uma base (nova versão)?
**R**: 
1. Criar nova pasta `data/raw/{base}_v2/`
2. Colocar novo arquivo com versionamento
3. Atualizar `metadata*.json` com data e versão
4. Nunca sobrescrever original

### P: Quando faço análise, onde salvo meus gráficos?
**R**: 
- Gráficos finais para artigo: `outputs/figures/`
- Tabelas para artigo: `outputs/tables/`
- Explorações pessoais: manter em branch local (não fazer commit)

---

**Documento revisado**: 2026-09-21  
**Próxima revisão recomendada**: Após integração de Acervo Folha  
**Responsável por manutenção**: Gustavo Paccelli
