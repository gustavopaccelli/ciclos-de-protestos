# Protocolo AEP–BEP: âncora metodológica do pipeline `protest_events`

**Referência canônica:** Alonso, A.; Rezende, P. J.; Souza, R. de; Souza, V. B. de.
"Análise de Eventos de Protesto: decisões metodológicas na organização do Banco de
Eventos de Protesto (BEP) 2013-2016." *Plural — Revista do PPG em Sociologia da USP*,
v. 31.2, jul./dez. 2024, p. 288-323.
DOI: https://doi.org/10.11606/issn.2176-8099.pcso.2024.233335

Este documento extrai as decisões metodológicas do artigo e as mapeia para o pipeline
`protest_events` deste projeto. Deve ser lido em conjunto com
`pipeline/config/doca_codebook.yaml` e `pipeline/docs/TUTORIAL.md`.

---

## 1. Fundamento epistemológico-teórico

### 1.1 Filiação teórica

A AEP deriva da **Teoria do Confronto Político** (TCP — McAdam, Tarrow, Tilly 2001),
que propõe uma sociologia relacional da mobilização centrada na interação entre atores
institucionais e não-institucionais. A consequência metodológica é tomar o **evento de
protesto** como unidade de análise, e não os atores ou as organizações — o que evita a
seleção *ex ante* de quais grupos são "relevantes" e mantém a abertura ao caráter
emergente e imprevisível da política de rua.

Implicação para o projeto: o pipeline `protest_events` é o braço empírico da pergunta
sobre EOP e DOS. A neutralidade da definição de evento (ver §2) é condição para não
enviesar a amostra em favor de atores/pautas previamente hipotetizados.

### 1.2 Estrutura sintática (Franzosi) + dimensão simbólica (Benford & Snow)

O BEP combina:
- **Estrutura ator–ação–objeto** (Franzosi 2004): preserva as relações sem dissolver
  atores, alvos e ações em variáveis apartadas. Ex.: "manifestantes–fechar–avenidas".
- **Dimensão semântica/simbólica**: slogans, bandeiras, performances corporais
  codificados como variáveis autônomas, captando os *frames* interpretativos
  (Benford & Snow 2000) que ampliam a ressonância das demandas.

Implicação: o `event_schema` do codebook DoCA mantém `repertoire` (ação) + `claim_text`
(semântica) como campos independentes, não colapsados.

### 1.3 Vieses de fonte e seu controle

Toda fonte jornalística carrega **viés de seleção** (quais eventos noticiados) e
**viés de descrição** (como a notícia enquadra). Controles adotados pelo BEP:
- **Diversificação de fontes**: Folha de S.Paulo (primária, maior circulação, mais
  detalhe) + G1 (secundária, capilaridade regional, cobertura de eventos pequenos).
- **92% de concordância** entre Folha e Estadão em junho de 2013 → a Folha como
  fonte única principal é defensável para ciclos de alta intensidade.
- **Pressuposto de sobre-noticiação em ciclos**: ciclos de confronto são super-cobertos;
  as notícias se corrigem e complementam mutuamente.

Implicação para o projeto: o `01_scraper.py` usa Acervo Folha como fonte primária.
Quando e se disponível, G1/outros portais devem ser usados como fonte secundária para
enriquecer variáveis com muitos `null`s (especialmente `crowd_size_reported` e `location`
para eventos menores). O campo `source_url` no schema permite rastrear a fonte por evento.

---

## 2. Definição operacional de evento de protesto

Um evento de protesto é:

| Critério | Descrição |
|----------|-----------|
| **1. Ação pública e coletiva** | Envolve múltiplos participantes em espaço público ou de acesso público |
| **2. Organizada por atores não estatais** | Excluem-se solenidades oficiais de governo |
| **3. Contestação** | Crítica a instituições, práticas ou valores — não pressupõe direção progressista |
| **4. Reivindicações sociais e/ou políticas** | Explícitas (slogans, bandeiras) ou mediadas por símbolos |

**Exclusões canônicas:**
- Ações individuais em nome próprio (não como representante de grupo)
- Ações coletivas exclusivamente disruptivas sem reivindicação (criminalidade comum)
- Ações lúdicas sem contestação (festas, jogos)
- Atos políticos rotineiros não-contestatórios (reuniões, convenções)
- Eventos realizados apenas no âmbito virtual
- Eventos **anunciados mas sem evidência de realização** confirmada na fonte

Esta definição é implementada no campo `eligible: bool` do `event_schema`. O DoCA coder
deve marcar `eligible: false` e registrar o motivo em `notes` para qualquer item excluído.

---

## 3. Seleção de fontes e palavras-chave

### 3.1 Palavras-chave validadas pelo BEP

O BEP testou múltiplas palavras-chave antes de fixar o conjunto abaixo como o de maior
eficiência na captura de notícias relevantes:

```
manifestação / manifestante / manifestar
protesto / protestar
reivindicar / reivindicação
greve / grevistas / paralisação
passeata
concentração
ato (protesto)
baderna / baderneiros / vândalos
depredação
black bloc
```

Estas palavras estão refletidas em `pipeline/config/queries.yaml`. Ao expandir para
novos períodos ou temas, testar novas palavras em amostra antes de incorporar ao conjunto
principal.

### 3.2 Fluxo de triagem

1. **Crawling** (scraper): captura íntegra da notícia com data, URL e palavra-chave usada.
2. **Triagem editorial** (step 1 — leitura do título): identificar palavras indicativas
   de protesto.
3. **Triagem por definição** (step 2 — leitura integral): aplicar os 4 critérios do §2
   e marcar como relevante (`limpa`) ou descartar.
4. **Codificação** por codificador.
5. **Validação** pela editoria: checar duplicatas, cruzar ID de evento.

No pipeline automatizado, os passos 2–5 são executados pelo `02_doca_coder.py` com
supervisão humana amostral (ver `04_intercoder_reliability.py` para Cohen's Kappa).

---

## 4. Unidade de análise: evento ≠ notícia

**Regra central**: a unidade do banco é o **evento**, não a notícia.
- Múltiplos eventos em uma notícia → desmembrar.
- Uma mesma notícia + notícias posteriores sobre o mesmo evento → agrupar sob um único ID.

### 4.1 Critérios de continuidade (mesmo evento)

| Dimensão | Regra |
|----------|-------|
| **Temporal** | Intervalo < 24h entre ações dos mesmos atores = um evento |
| **Temporal (duração > 24h)** | Ação contínua sem interrupção (ex. ocupação de 5 dias) = um evento |
| **Temporal (intervalo > 24h)** | Ações dos mesmos atores com descontinuidade > 24h = eventos distintos |
| **Espacial** | Mesma localidade + mesmos/similares atores (mesmo com trajetos distintos) = um evento |
| **Espacial (local não especificado)** | Mesmos participantes + objetivos semelhantes = um evento |

### 4.2 Critérios de separação (eventos distintos)

| Situação | Regra |
|----------|-------|
| Mesmos atores, localidades **distintas e nomeadas** | Eventos distintos (mesmo tema/ciclo) |
| Atores com **pautas opostas** em trajetos coincidentes | Eventos distintos (separar por organizador) |
| Ações planejadas/anunciadas **sem confirmação de realização** | Excluir |

O campo `event_id` no schema é um UUID5 determinístico calculado sobre `(source_url, event_date, location_city)`. Conflitos de ID sinalizam possível duplicata e requerem revisão manual.

---

## 5. Estrutura de variáveis — 5 blocos BEP mapeados ao schema DoCA

O BEP organiza variáveis em 5 blocos. A tabela abaixo mapeia cada bloco ao campo
correspondente no `event_schema` de `doca_codebook.yaml`.

### Bloco I — Identificação do evento

| Variável BEP | Campo DoCA | Obs. |
|---|---|---|
| ID | `event_id` | UUID5 determinístico |
| Data | `event_date` | Data do EVENTO, não da publicação |
| Local do evento | `location_venue` | Todos os locais do trajeto |
| Tipo de local (8 cat.) | `location_venue_type` | Fechado (novo campo) |
| Uso convencional/não convencional | `location_conventional` | Bool (novo campo) |
| Cidade | `location_city` | |
| Porte da cidade (3 cat.) | `city_size` | Estatuto da Cidade: <20k / 20-50k / >100k |
| Estado | `location_state` | Sigla |
| Número de manifestantes (polícia/imprensa/organizadores) | `crowd_size_reported` | Registrar o maior valor |
| Porte da manifestação (4 cat.) | `crowd_size_scale` | Alinhado ao BEP (ver §6) |

### Bloco II — Atores coletivos

| Variável BEP | Campo DoCA | Obs. |
|---|---|---|
| Nome do ator | `actors[].name` | Prioridade: sigla+nome > categoria MS > "manifestantes" |
| Especificação do ator | `actors[].specification` | Subgrupos, indivíduos nomeados |
| Forma de organização (7 cat.) | `actors[].org_type` | Ver §6 |
| Formalização (formal/informal) | `actors[].formalization` | Ver §6 |

### Bloco III — Performances políticas

| Variável BEP | Campo DoCA | Obs. |
|---|---|---|
| Tipos de ação — verbo | `repertoire` | Infinitivo ou substantivo canônico |
| Tipos de ação — objeto | `action_object` | Novo campo |
| Tipos de ação — instrumento | `action_instrument` | Novo campo |
| Símbolos (bandeiras, signos visuais/corporais) | `symbols` | Novo campo (lista) |

### Bloco IV — Temas e slogans

| Variável BEP | Campo DoCA | Obs. |
|---|---|---|
| Temas | `claim_code` + `claim_text` | code = domínio, text = demanda livre |
| Slogans | `slogans` | Novo campo (lista, grafia original) |

### Bloco V — Resposta das autoridades / interação entre manifestantes

| Variável BEP | Campo DoCA | Obs. |
|---|---|---|
| Presença de conflito | `conflict_present` | Bool |
| Conflito com forças de segurança | `conflict_police` | Bool (= `repression != "none"`) |
| Conflito entre manifestantes | `conflict_inter_group` | Bool (novo campo) |
| Número de presos | `arrests_reported` | Int ou null |
| Número de feridos | `injuries_reported` | Int ou null |

> **Nota de implementação**: o campo `repression` (none / dispersão / prisões / violência)
> já captura `conflict_police`. Manter `conflict_present` como flag agregada.

---

## 6. Dicionários de valores — alinhamento BEP

### 6.1 Porte da manifestação (BEP — usar como padrão)

| Categoria | Intervalo |
|---|---|
| Pequena | até 2.000 manifestantes |
| Média | 2.001 – 10.000 |
| Grande | 10.001 – 100.000 |
| Mega | mais de 100.000 |

> **Diferença do schema anterior**: o codebook DoCA original usava escala 0-5 ordinal.
> Manter a escala 0-5 para compatibilidade com saída do LLM, mas documentar o
> mapeamento: 0=SI, 1=até100, 2=101-1000, 3=1001-10000, 4=10001-100000, 5=>100000.
> A categorização BEP (pequena/média/grande/mega) é derivada do valor numérico reportado.

### 6.2 Tipo de local (Bloco I, var. 4)

`estabelecimento-comercial` | `instituição-cultural-ensino` | `instituição-religiosa` |
`órgão-sistema-viário` | `órgão-poder-público` | `praça-via-pública` | `rodovia` |
`sede-partido-político` | `SI`

### 6.3 Uso convencional do local

- **Convencional**: praça/via pública, instituição cultural/ensino, órgão/sede poder público, sede partidária
- **Não convencional**: estabelecimento comercial, instituição religiosa, rodovia, órgão sistema viário

### 6.4 Forma de organização dos atores (var. 13)

`associação-civil` | `associação-empresarial` | `igreja` | `movimento-social` |
`partido-político` | `sindicato` | `manifestantes` (sem organização identificada)

### 6.5 Formalização dos atores (var. 14)

- **Formal**: agrupamento formalizado/institucionalizado, mencionado pelo nome
- **Informal**: agrupamento reconhecível, mas sem indício de institucionalização

### 6.6 Verbos canônicos de ação (seleção BEP)

Registrar no infinitivo; sinônimos devem convergir para o verbo mais geral:
`agredir` | `arremessar` | `bloquear` | `concentrar` | `greve` | `incendiar` |
`marchar` | `ocupar` | `panfletar` | `passeata` | `peticionar` | `pichar` |
`quebrar` | `saquear` | `assembleia` | `barricada` | `vigília` | `panelaço`

---

## 7. Estratégia de codificação

O BEP usa **codificação mista** (*bottom-up* + *top-down*):
1. Primeiro registro aberto: valores coletados como aparecem na notícia.
2. Recategorização posterior: aplicar códigos fechados ao material compilado.

No pipeline automatizado (`02_doca_coder.py`), o LLM produz valores em texto livre que
são normalizados pelo `03_build_dataset.py` contra os dicionários do codebook. Variáveis
com >30% de `null` após triangulação de fontes devem ser excluídas da análise final
(conforme decisão BEP para variáveis com excesso de *missings*).

---

## 8. Agenda futura e uso de IA

Alonso et al. (2024, p. 320) identificam explicitamente que:
> "Ferramentas de processamento de linguagem natural raspam grandes volumes de notícias,
> identificam eventos e mesmo procedem à alimentação de variáveis de modo semi-automático.
> Nesse sentido, as IAs vieram para ficar na pesquisa sobre protestos."

Ao mesmo tempo, alertam:
> "A demarcação da amostra e os critérios de codificação dependem de um bom desenho de
> pesquisa, que, por sua vez, depende da experiência e da destreza analítica de um
> pesquisador teoricamente informado."

**Implicação direta para este projeto**: o `02_doca_coder.py` com API Anthropic é
metodologicamente legítimo dentro do Protocolo BEP — desde que:
- O system prompt esteja ancorado nas definições do §2 e §4 deste documento
- A confiabilidade inter-codificadores seja aferida por `04_intercoder_reliability.py`
  (Cohen's Kappa ≥ 0,75 como threshold mínimo aceitável)
- Variáveis ambíguas recebam revisão editorial amostral

---

## 9. Contribuição epistemológica para o projeto

| Contribuição | Implicação |
|---|---|
| **Neutralidade axiológica da definição de evento** | O banco não pressupõe que protestos são progressistas — permite capturar tanto ciclos de esquerda (Diretas Já, Junho 2013) quanto de direita (ciclo patriota 2015-2016) na mesma grade |
| **Abordagem relacional (TCP)** | Alinha com o quadro teórico EOP+DOS: o evento como produto de interações entre atores desafiadores e autoridades confirma a centralidade das oportunidades relacionais |
| **Combinação sintaxe + semântica** | Conecta repertório de confronto (Tilly) com enquadramentos discursivos (Benford & Snow) — exatamente o que a tese precisa para articular EOP (estrutural) e DOS (discursiva) |
| **Codificação de respostas das autoridades** | O Bloco V captura a dimensão repressiva que é variável-chave em H1 (efeito da repressão sobre escala do ciclo) |
| **Escala de porte da manifestação** | Fornece medida de "densidade demográfica" dos eventos, essencial para testar hipóteses sobre a relação entre tamanho do ciclo e resultado institucional |
| **Série histórica possibilitada pela IA** | Permite expandir o BEP para os ciclos anteriores (Diretas Já, Fora Collor) — hoje inviáveis manualmente — e produzir séries longas que fundamentam comparações temporais rigorosas |

---

## 10. Evento canônico e deduplicação entre fontes

*Incorporado a partir de: Hanna, A. MPEDS: Machine-Learning Protest Event Data System (v1.0). Zenodo, 2017. DOI: 10.5281/zenodo.886459*

### 10.1 O problema da deduplicação

Um mesmo evento de protesto pode ser coberto por múltiplos artigos na mesma fonte (notícia do dia + cobertura posterior) ou por diferentes fontes. Sem deduplicação, o banco infla artificialmente a contagem de eventos e distorce variáveis de tamanho e intensidade.

O MPEDS distingue três níveis:

| Nível | Definição | Campo DoCA |
|---|---|---|
| **Artigo** | Texto jornalístico individual, unidade de entrada do scraper | `source_url` |
| **Evento codificado** | Extração do LLM a partir de um artigo; pode haver múltiplos eventos por artigo | `event_id` (UUID5) |
| **Evento canônico** | Evento único após agrupamento de registros que descrevem o mesmo episódio real | `canonical_event_id` |

### 10.2 Critério de canonização

Dois eventos codificados (possivelmente de artigos diferentes) são agrupados em um evento canônico quando:
1. As datas coincidem ou se sobrepõem (critérios de continuidade temporal do §4.1).
2. A localidade é a mesma ou contígua (critério espacial do §4.1).
3. Os atores principais e as reivindicações são compatíveis.

O `canonical_event_id` é atribuído manualmente pelo editor na etapa de validação (ver §10.4) ou por algoritmo de deduplicação no `03_build_dataset.py` (implementação futura).

### 10.3 Artigos com múltiplos eventos

Quando um artigo relata dois ou mais eventos de protesto distintos (ex.: "protestos simultâneos em SP e RJ"), o campo `multi_event_article: true` sinaliza que o `02_doca_coder.py` deve desmembrar a notícia e produzir múltiplos registros no JSON de saída, cada um com seu próprio `event_id`.

### 10.4 Fluxo de canonização

```
Artigo → scraper → JSON bruto (event_id por linha)
                           ↓
           03_build_dataset.py — clustering por (data, cidade, ator_principal)
                           ↓
           Editor humano — revisão de conflitos de ID e atribuição de canonical_event_id
                           ↓
           Dataset final — uma linha por evento canônico
```

---

## 11. Workflow multi-passagem

*Adaptado do fluxo MPEDS (Hanna 2017) para o pipeline DoCA/BEP.*

O pipeline `protest_events` opera em 5 passagens sequenciais. Cada passagem tem entrada, processamento e saída definidos:

### Passagem 1 — Captura (01_scraper.py)

| Item | Descrição |
|---|---|
| Entrada | Palavras-chave de `queries.yaml`; período de busca |
| Processamento | Login no Acervo Folha; busca incremental por data; captura de HTML/texto da notícia |
| Saída | Arquivo JSONL com `{source_url, source_date, headline, body_text, query_used}` |

### Passagem 2 — Triagem (02_doca_coder.py, step 1)

| Item | Descrição |
|---|---|
| Entrada | JSONL da Passagem 1 |
| Processamento | LLM aplica critérios §2: marca `eligible: bool`; se `false`, registra motivo em `notes` |
| Saída | JSONL filtrado com campo `eligible` preenchido |

### Passagem 3 — Codificação (02_doca_coder.py, step 2)

| Item | Descrição |
|---|---|
| Entrada | Registros com `eligible: true` |
| Processamento | LLM preenche todos os campos do `event_schema` (Blocos I–V + campos MPEDS) |
| Saída | JSONL com event_schema completo; `multi_event_article` sinaliza desmembramento |

### Passagem 4 — Construção do dataset (03_build_dataset.py)

| Item | Descrição |
|---|---|
| Entrada | JSONL da Passagem 3 |
| Processamento | Normalização contra dicionários do codebook; clustering para `canonical_event_id`; exportação CSV/XLSX |
| Saída | `protest_events.csv` (uma linha por evento canônico) + `protest_events_raw.csv` (uma linha por extração) |

### Passagem 5 — Confiabilidade (04_intercoder_reliability.py)

| Item | Descrição |
|---|---|
| Entrada | Amostra aleatória (≥10% do corpus) recodificada por codificador humano independente |
| Processamento | Cálculo de Cohen's Kappa por variável |
| Saída | Relatório de confiabilidade; variáveis com Kappa < 0,75 ou missing > 30% são sinalizadas para revisão do system prompt ou exclusão da análise |
