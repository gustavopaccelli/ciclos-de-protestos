# Livro de Código — Mass Mobilization (MM) Data Project

> **Fonte original:** CLARK, David H.; REGAN, Patrick M. *Mass Mobilization Protest Data.* Codebook and User's Manual, May 2015 (manual preservado em `../fonte-original/MM_users_manual_0515.pdf`). Arquivo de dados: `mmALL_073120` (versão v16, 31/07/2020), que estende a cobertura para **1990–2020**.
> Transcrição/síntese estruturada em Markdown. O conteúdo conceitual é dos autores; formatação adaptada para versionamento.

Financiamento: Political Instability Task Force. Distribuição: Harvard Dataverse.

---

## Escopo e unidade de observação

- **Unidade:** protesto–país–ano (cada protesto registrado individualmente por país e ano).
- **Cobertura:** 162 países, **1990–2020** (o manual de 2015 descreve 1990–2014; o arquivo v16 estende até 2020).
- **Subconjunto neste projeto:** apenas **Brasil** (`ccode = 140`, Polity), **224 registros** — extraídos do arquivo global conforme instrução do usuário ("somente os dados sobre protestos no Brasil").

## Definição de protesto (critérios de inclusão)

Protesto = **reunião de 50 ou mais pessoas** para fazer uma **demanda ao governo**. A ação deve ter como **alvo o Estado ou uma política estatal** ("home grown", contra o próprio Estado).

**Exclusões canônicas:**
- Protestos contra políticas de **outro país**.
- **Conflitos intercomunais** (grupos sociais entre si, sem alvo estatal).
- **Ataques de rebeldes** ou resistência armada ao Estado.
- **Comícios político-partidários** (rallies eleitorais — considerados pró-Estado).
- Ações sindicais restritas a uma empresa específica, salvo quando se tornam evento público de rua com demanda ao Estado.

## Método de coleta

Busca no **Lexis-Nexis "All News"** ("major world publications") por quatro termos unidos por OR: *Protest, Demonstration, Riot, Mass Mobilization*. Fontes primárias: *New York Times, Washington Post, Christian Science Monitor, Times of London* (+ *Jerusalem Post* no MENA); expansão regional quando < 100 artigos.

---

## Dicionário de variáveis (31 colunas)

| Coluna | Descrição |
|---|---|
| `id` | Identificador único do caso (ccode+ano+nº) |
| `country`, `ccode` | Nome e código Polity do país (Brasil = 140) |
| `year` | Ano |
| `region` | Região (Brasil = South America, códigos 100–165) |
| `protest` | Dicotômica: houve protesto no período (todos = 1 no subconjunto Brasil) |
| `protestnumber` | Número do protesto no ano |
| `startday/startmonth/startyear` | Data de início |
| `endday/endmonth/endyear` | Data de término (igual à de início em protesto de 1 dia) |
| `protesterviolence` | Dicotômica: manifestantes usaram violência contra o Estado (0/1) |
| `location` | Local do protesto (o mais específico possível; "national" se organização nacional) |
| `participants_category` | Faixa padronizada (ver abaixo) |
| `participants` | Estimativa bruta de participantes (usa o menor valor num momento; máximo se cresce ao longo dos dias) |
| `protesteridentity` | Nome/identidade do grupo organizador |
| `protesterdemand1..4` | Até 4 demandas (ver tabela de códigos) |
| `stateresponse1..7` | Até 7 respostas do Estado (ver tabela de códigos) |
| `sources` | Artigo(s) usados na codificação |
| `notes` | Informações que embasaram a decisão de codificação |

### Faixas de participação (`participants_category`)
`50-99` · `100-999` · `1000-1999` · `2000-4999` · `5000-10000` · `>10000`
(campo adicionado no meio da codificação — ausente em parte dos casos; no Brasil, 151 dos 224 registros estão vazios.)

### Tabela de códigos — Demandas dos manifestantes (7 categorias)

| # | Categoria (rótulo no dado) | Descrição |
|---|---|---|
| 1 | `labor wage dispute` | Demanda contra política estatal que afeta condições de trabalho ou salários |
| 2 | `land farm issue` | Acesso/restrições ao uso da terra por política estatal |
| 3 | `police brutality` | Tratamento arbitrário/brutalidade das autoridades contra cidadãos |
| 4 | `political behavior, process` | Categoria mais ampla: processo político, quem governa e como, reforma, transição democrática |
| 5 | `price increases, tax policy` | Subsídios, aumento de impostos, custo de alimentos/utilidades |
| 6 | `removal of politician` | Corrupção sistêmica que gera demanda pela remoção de indivíduo/grupo no governo |
| 7 | `social restrictions` | Restrições a interações entre grupos, proibição de comportamentos/direitos de um grupo |

### Tabela de códigos — Respostas do Estado (7 categorias)

| # | Categoria (rótulo no dado) | Descrição |
|---|---|---|
| 1 | `accomodation` | Acomodação: negociação, atendimento da demanda, reunião formal com a liderança |
| 2 | `arrests` | Prisões |
| 3 | `beatings` | Espancamentos |
| 4 | `crowd dispersal` | Dispersão (gás lacrimogêneo, avisos, deslocamento de tropas) |
| 5 | `ignore` | Ignorar (sem reação estatal reportada) |
| 6 | `killings` | Mortes |
| 7 | `shootings` | Disparos |

> Observação: o rótulo `accomodation` reproduz a grafia (com um "m") tal como consta no arquivo de dados original — preservado para fidelidade de valores.

---

## Distribuição do subconjunto Brasil (1990–2020)

- **224 protestos**, todos com `protest = 1`, `ccode = 140`.
- **Demanda primária** (`protesterdemand1`): political behavior/process (136), labor wage (42), removal of politician (23), price/tax (14), police brutality (5), land/farm (4).
- **Resposta estatal primária** (`stateresponse1`): ignore (140), crowd dispersal (62), accommodation (12), killings (4), shootings (3), arrests (3).
- **Violência dos manifestantes:** 39 de 224 (17%).
- **Picos anuais:** 2013 (23), 2015 (23), 2016 (23) — coincidem com Junho de 2013 e o ciclo do impeachment.

Ver `crosswalk-codigos.md` para o mapeamento (sem mesclagem) entre as categorias MM e os códigos já existentes no projeto.
