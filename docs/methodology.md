# Metodologia: Ciclos de Protesto no Brasil

**Projeto**: Análise Comparada de Ciclos de Protesto no Brasil (1985-2024)  
**Data de Criação**: 2026-09-20  
**Última Revisão**: 2026-09-20  
**Pesquisador Responsável**: Gustavo Paccelli  

---

## 1. Recorte Temporal

### Período Principal de Análise
**1985-2024** (~40 anos)

### Ciclos de Protesto Identificados

#### 1. Diretas Já (1983-1985)
- **Período**: 1983-1985
- **Evento Mobilizador**: Campanha pela reintrodução das eleições diretas para presidente
- **Contexto**: Transição democrática; fim da ditadura militar
- **Pico de Mobilização**: Abril-maio de 1985

#### 2. Fora Collor (1992)
- **Período**: 1991-1993
- **Evento Mobilizador**: Protestos contra corrupção e impeachment de Fernando Collor de Mello
- **Contexto**: Instabilidade política pós-democratização; conflito com presidente neoliberal
- **Pico de Mobilização**: Agosto-setembro de 1992

#### 3. Junho de 2013 (2011-2014)
- **Período**: 2011-2014
- **Evento Mobilizador**: Protestos contra aumento de tarifas de transporte; evolução para agenda ampla
- **Contexto**: Esgotamento de ciclo de "neodesenvolvimentismo"; ascensão de ocupações urbanas
- **Pico de Mobilização**: Junho-julho de 2013

#### 4. Impeachment de Dilma (2015-2016)
- **Período**: 2014-2016
- **Evento Mobilizador**: Mobilizações por/contra impeachment de Dilma Rousseff
- **Contexto**: Crise econômica; polarização política; fragmentação da coligação governamental
- **Pico de Mobilização**: Março-maio de 2016

---

## 2. Fontes de Dados

### 2.1 Fontes Primárias

#### a) Arquivos de Mídia
- **Jornais**: Folha de S.Paulo, O Globo, Estadão (cobertura de principais eventos)
- **Agências de Notícias**: EFE, Reuters, AP
- **Publicações**: Revistas especializadas (Estudos Avançados, Brazilian Review of Social Sciences)
- **Período**: Cobrindo cada ciclo + 6 meses antes/depois

#### b) Documentação Oficial
- **Arquivos do Congresso Nacional**: Discursos, moções, requerimentos
- **Documentos de Segurança**: Relatórios de inteligência (quando disponível)
- **Registros Municipais**: Comunicações ao DETRAN, polícia local
- **Base de Dados**: Atas de sessões, diários do Congresso

#### c) Fontes de Pesquisa Prévia
- **NEPAC Database** (Tatagiba et al., 2019): Protestos 2011-2016
- **Mass Mobilization Project** (Clark & Regan, 2020): Protestos 1990-2020
- **Acervo Folha**: Banco de dados de eventos (projetos temáticos)

### 2.2 Dados Externos Consolidados

| Fonte | Cobertura | Variáveis Chave | Acesso |
|-------|-----------|-----------------|--------|
| NEPAC | 2011-2016 | Tipo de ator, reivindicações, violência | dados/raw/bancos-externos/nepac-tatagiba-galvao-2019/ |
| Mass Mobilization | 1990-2020 | Data, localização, estimativa de tamanho | dados/raw/bancos-externos/mass-mobilization-clark-regan-2020/ |
| Acervo Folha | 1985-2016 | Eventos Diretas Já e cobertura geral | Scrapyng via pipeline/01_scraper.py |

---

## 3. Procedimentos de Coleta

### 3.1 Web Scraping e Digitalização
- **Ferramenta Principal**: Python (Selenium, BeautifulSoup)
- **Alvo**: Portais de jornais, bases de dados públicas
- **Script**: `src/data/scraper.py`
- **Saída**: Textos brutos, URLs, metadados de publicação

### 3.2 Extração de Dados Estruturais
- **Série Temporal Legislativa**: `src/data/pt_extrai_legislativo.py`
  - Discursos, votações, comissões relacionadas a cada ciclo
  
- **Indicadores Estruturais**: `src/data/pt_extrai_series.py`
  - Taxa de desemprego, inflação, aprovação presidencial
  - Fontes: IBGE, Banco Central, DataFolha

### 3.3 Integração de Bases Externas
- **Importação**: Arquivos XLSX/CSV das bases NEPAC e Mass Mobilization
- **Padronização**: Alinhamento de variáveis comuns
- **Script**: `src/data/pt_gera_planilha_fontes.py`

---

## 4. Critérios de Inclusão/Exclusão

### 4.1 Inclusão de Eventos

Um evento é incluído se:

1. **Ocorreu dentro do recorte temporal**: 1985-2024
2. **É um evento de ação coletiva contentious**: Manifestação, protesto, comício, bloqueio, ocupação, acampamento
3. **Envolve cidadãos/sociedade civil**: Não apenas elites parlamentares
4. **Tem um objetivo político/social explícito**: Reivindicação ou contestação de autoridade
5. **Possui documentação mínima**: Pelo menos uma fonte confiável (jornal, relatório, arquivo)

### 4.2 Exclusão de Eventos

Eventos são excluídos se:

1. **São atividades rotineiras**: Reuniões de partidos, sessões parlamentares sem mobilização
2. **São eventos institucionais**: Eleições, posse de autoridades (sem confronto)
3. **Violência sem contexto de protesto**: Crimes comuns, agressões isoladas
4. **Informação muito vaga**: Sem data específica, localização desconhecida, fonte duvidosa
5. **Duplicação**: Mesmo evento coberto em múltiplas fontes (manter referência cruzada)

---

## 5. Procedimentos de Codificação

### 5.1 Esquema de Codificação

**Variáveis Principais Codificadas**:
- Identificação do evento (ID único, data, localização)
- Características (tipo de ação, tamanho estimado, reivindicações)
- Atores (partidos, sindicatos, movimentos, sociedade civil)
- Confrontação (violência, repressão, prisões)
- Cobertura mediática (fonte, confiabilidade)

**Referência**: `docs/codebook/cycle_phases_codebook.yaml`

### 5.2 Ferramenta de Codificação
- **Sistema**: DOCA (Document Annotation) via aplicação custom
- **Scripts**: 
  - `src/preprocessing/coder.py` - Interface de codificação
  - `src/preprocessing/intercoder_reliability.py` - Teste de confiabilidade

### 5.3 Treinamento de Codificadores

1. **Familiarização**: Leitura de guia de codificação + 5 exemplos anotados
2. **Treino Independente**: Codificar 20 eventos, comparar com gabarito
3. **Iteração**: Esclarecimento de dúvidas, ajuste de interpretações
4. **Validação**: Alcançar Krippendorff's alpha ≥ 0.70 em amostra de overlap

### 5.4 Confiabilidade Entre Codificadores

- **Método**: Dupla-codificação de ~10% da amostra por ciclo
- **Estatística**: Krippendorff's alpha para variáveis nominais
- **Limite Aceitável**: α ≥ 0.70 (moderada a alta confiabilidade)
- **Script de Cálculo**: `src/preprocessing/intercoder_reliability.py`
- **Histórico**: `docs/codebook/historico-codificacao.csv`

---

## 6. Processamento e Limpeza de Dados

### 6.1 Etapas de Processamento

**Fase 1: Padronização** (`src/preprocessing/`)
- Normalização de nomes de cidades (grafia, abreviaturas)
- Padronização de datas (verificação de impossibilidades)
- Categorização de tipos de eventos
- Limpeza de duplicatas

**Fase 2: Validação** (`src/preprocessing/valida_cycle_phases.py`)
- Verificação de campos obrigatórios
- Validação de tipos de dados
- Detecção de outliers (ex: tamanho de evento impossível)
- Consistência de relacionamentos (ex: evento deve estar em um ciclo válido)

**Fase 3: Enriquecimento** (`src/analysis/build_series_temporais.py`)
- Cálculo de séries temporais (eventos por mês, por semana)
- Derivação de variáveis (dias desde início de ciclo, posição no ciclo)
- Agregação geográfica (eventos por estado, região)

### 6.2 Gestão de Valores Ausentes

| Variável | Estratégia |
|----------|-----------|
| Data | Excluir evento (informação crítica) |
| Localização | Usar "localização desconhecida" se região está disponível |
| Tamanho | Codificar como "desconhecido"; não imputar |
| Atores | Deixar em branco se não identificável; não assumir |
| Reivindicações | Usar texto de fonte se disponível; marcar como "vago" se necessário |

---

## 7. Análise de Dados

### 7.1 Estatísticas Descritivas
- Contagens de eventos por ciclo, período, localização
- Distribuição de tipos de eventos e atores
- Evolução temporal de indicadores-chave

### 7.2 Análise Comparativa Entre Ciclos
- Duração de cada ciclo e suas fases
- Composição de atores (similar/diferente entre ciclos?)
- Escalonamento de confrontação (violência, repressão)
- Êxito/êxito parcial em reivindicações

### 7.3 Process Tracing de Ciclos Específicos
- Mapeamento de causalidade entre eventos (Diretas Já → reemocratização)
- Análise de pontos de inflexão em cada ciclo
- Documentação de documentos primários (ver `docs/process_tracing_*/`)

---

## 8. Documentação e Reprodutibilidade

### 8.1 Estrutura de Arquivos
```
repository/
├── data/
│   ├── raw/              # Dados originais (não modificados)
│   ├── interim/          # Dados intermediários
│   └── processed/        # Dados finais processados
├── src/
│   ├── data/            # Scripts de extração/coleta
│   ├── preprocessing/   # Scripts de limpeza e validação
│   └── analysis/        # Scripts de análise
├── docs/                # Documentação completa
│   ├── codebook.md      # Este arquivo (variáveis)
│   ├── methodology.md   # Este documento (procedimentos)
│   ├── artefatos/       # Documentos de pesquisa
│   ├── experiments/     # Protocolos por ciclo
│   └── process_tracing/ # Documentação de process tracing
└── outputs/
    ├── figures/         # Gráficos e visualizações
    └── tables/          # Tabelas compiladas
```

### 8.2 Replicabilidade
- **Requisitos**: Ver `requirements.txt`
- **Instalação**: `pip install -r requirements.txt`
- **Configuração**: Ver `.env.example` para variáveis de ambiente
- **Execução do Pipeline**: `python src/analysis/run_pipeline.py`

### 8.3 Controle de Versão
- **Sistema**: Git
- **Branch Padrão**: main (stable) e development (in-progress)
- **Commits**: Cada mudança documentada com mensagem clara

---

## 9. Questões Metodológicas Abertas

1. **Tamanho de eventos**: Estimativas de mídia costumam variar significativamente
   - *Abordagem*: Registrar múltiplas estimativas; usar escala categórica

2. **Atribuição causal**: Difícil determinar se evento A causou evento B
   - *Abordagem*: Usar process tracing qualitativo como complemento

3. **Representação de minorias**: Jornais cobrem melhor eventos em capitais/grandes cidades
   - *Abordagem*: Usar múltiplas fontes; alertar sobre viés geográfico em análises

---

## 10. Referências Metodológicas

- Della Porta, D., & Diani, M. (2006). Social Movements: An Introduction.
- Tilly, C. (2004). Social Movements, 1768-2004.
- Tatagiba, L., Galvão, A., & Trindade, T. (2019). Movimentos Sociais no Brasil (NEPAC Database).
- Clark, D., & Regan, P. (2020). Mass Mobilization Protests Database.

---

## 11. Contato e Revisões

**Responsável Técnico**: Gustavo Paccelli  
**Email**: gustavopaccelli@gmail.com  
**Última atualização**: 2026-09-20  

Para sugestões de melhorias metodológicas, abra uma issue no repositório.
