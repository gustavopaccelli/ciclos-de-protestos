# Ciclos de Protesto no Brasil: Estruturas de Oportunidades Políticas, Estruturas de Oportunidades Discursivas e Análise de Conjuntura

**Autor:** Gustavo Paccelli Costa (UFJF)
**Status:** pesquisa em andamento — repositório de trabalho (preprint em consolidação)
**Casos:** Diretas Já (1983–1984) · Fora Collor (1992) · Junho de 2013 · Impeachment de Dilma Rousseff (2014–2016)

---

## Resumo

Este projeto investiga como as configurações das **estruturas de oportunidades políticas (EOP)** e das **estruturas de oportunidades discursivas (DOS)**, lidas conjunturalmente pelos atores, condicionam a emergência, a dinâmica de fases e os desfechos dos ciclos de protesto no Brasil. Propõe-se a integração analítica de três tradições: a Teoria do Processo Político (TPP), a literatura sobre oportunidades discursivas e a tradição brasileira de **análise de conjuntura** — formando o triângulo EOP–DOS–Conjuntura. A proposta é testada em um estudo comparativo dos quatro principais ciclos de mobilização multisetorial da redemocratização brasileira, combinando periodização formalizada em fases, codificação ordinal de variáveis institucionais e discursivas, *process tracing* e Análise de Eventos de Protesto (AEP). O projeto dá continuidade à investigação doutoral de Costa (2024, UFJF) sobre estruturas de mobilização e oportunidades políticas nos ciclos de protesto do Brasil contemporâneo.

**Palavras-chave:** ciclos de protesto; estrutura de oportunidades políticas; estrutura de oportunidades discursivas; análise de conjuntura; movimentos sociais; Brasil.

---

## 1. Introdução

A tradição intelectual brasileira tem na **análise de conjuntura** uma de suas ferramentas mais duradouras e politicamente consequentes — dos manuais dos movimentos sociais das décadas de 1970–80 (Souza, 1986) às sistematizações recentes (Jatobá, 2025; Virgens & Teixeira, 2023). Essa tradição, contudo, opera majoritariamente com categorias desenvolvidas internamente (atores, forças, arenas, correlação de forças), sem diálogo sistemático com o instrumental que a sociologia dos movimentos sociais acumulou nas últimas quatro décadas — em particular a **Teoria do Processo Político** (Tarrow, 1994; McAdam, 1982) e a literatura sobre **oportunidades discursivas** (Koopmans & Statham, 1999; Ferree, 2003). Inversamente, a TPP raramente incorpora as leituras situadas e historicamente ancoradas que a análise de conjuntura produz sobre contextos específicos.

Este projeto parte da hipótese de que essa lacuna é simultaneamente um problema teórico e uma limitação prática:

- **Teórico** — a análise de conjuntura carece de instrumentos para distinguir, no interior de uma mesma conjuntura, as condições **político-institucionais** que constrangem ou viabilizam a ação coletiva (EOP) das condições **simbólico-discursivas** que determinam quais demandas podem ser articuladas com eficácia na esfera pública (DOS).
- **Prático** — os atores que usam a análise de conjuntura como ferramenta estratégica ficam privados de categorias para ler com precisão quando as "linhas de fratura" se abrem e quais enquadramentos encontram ressonância nesses momentos.

A integração proposta não substitui uma tradição pela outra: a EOP oferece à análise de conjuntura uma teoria das janelas de oportunidade institucionais; a DOS acrescenta uma teoria das condições culturais e comunicativas de legitimidade dos *frames*; e a análise de conjuntura oferece à TPP um instrumental interpretativo situado e sensível à temporalidade dos processos históricos.

Para demonstrar a fertilidade dessa integração, o projeto compara os **quatro principais ciclos de protesto de massa da redemocratização**: as Diretas Já (caso de origem da gramática contenciosa democrática, ainda sob regime autoritário em liberalização), o Fora Collor, Junho de 2013 e o ciclo do impeachment de Dilma Rousseff. Da comparação emergem **quatro padrões de articulação EOP–DOS**:

1. **Convergência EOP+DOS** (Fora Collor) → mobilização massiva com resultado institucional previsível;
2. **Abertura caótica EOP+DOS** (Junho 2013) → alta mobilização sem resultado institucional definido;
3. **Construção deliberada de EOP+DOS** (Impeachment) → resultado definido por atores estratégicos que produziram as próprias oportunidades;
4. **Assimetria de DOS** → polarização, disputa de legitimidade e legados discursivos que pré-moldam o ciclo seguinte.

---

## 2. Quadro geral metodológico

O desenho é uma **comparação qualitativa de casos** (N=4) com codificação formalizada e *process tracing* analítico (Beach & Pedersen, 2013), organizado em quatro componentes:

### 2.1 Periodização em fases (v3)

Cada ciclo é decomposto em **fases analíticas** — articulação, emergência, expansão, pico, latência, radicalização, declínio e desfecho — totalizando **24 fases** (6 por ciclo) no dataset `data/cycle_phases.csv`. Decisões notáveis, ancoradas na tese de Costa (2024):

- **Fases de articulação** identificadas nas Diretas Já, no Fora Collor (nov/1991–mai/1992, via Mische, 2008) e no Impeachment (a partir de 27/10/2014, dia seguinte à derrota eleitoral contestada de Aécio Neves — confronto eleitoral, McAdam & Tarrow, 2011). **Junho de 2013 não possui fase de articulação**: a pré-história autonomista dos anos 2000 é esparsa, não uma articulação deliberada.
- **Radicalização** em Junho 2013 (pós-pico, após a violência policial de 13/06 e a saída do MPL).
- **Latência** no ciclo do Impeachment (ago–dez/2015).

Justificativas completas em `docs/periodizacao-articulacao.md`.

### 2.2 Codificação ordinal (9 variáveis, escala 0–3)

Para cada fase são codificadas **5 variáveis de EOP** (abertura do sistema, vulnerabilidade das elites, aliados influentes, repressão, instabilidade de alinhamentos), **3 variáveis de DOS** (ressonância dos frames, visibilidade/valência midiática, hegemonia discursiva) e a variável **`traducao_institucional`** (0–3), que captura quando o resultado do ciclo é obtido por canal institucional distinto do demandado (ex.: as Diretas Já perdem a emenda Dante de Oliveira, mas elegem Tancredo no Colégio Eleitoral). Codebook completo: `codebook/cycle_phases_codebook.yaml`. Código `NA` distinto de `0` (não se aplica ≠ ausente).

### 2.3 Análise de Eventos de Protesto (AEP)

- **Âncora metodológica:** Protocolo **BEP-CEBRAP** (Alonso et al., 2024, *Plural* 31.2) — definição de evento, seleção de fontes, 5 blocos de variáveis, critérios de continuidade espaço-temporal, deduplicação por evento canônico (ver `docs/aep-protocol-bep.md`).
- **Pipeline** (`pipeline/`): scraper do Acervo Folha → codificador DoCA assistido por LLM (codebook alinhado a BEP + campos MPEDS) → construção do dataset → confiabilidade intercodificador (Kappa ≥ 0,75). Execução aguarda credenciais do Acervo Folha.
- **Sementes manuais** (`data/protest_events_seeds/`): Diretas Já (59 eventos) e Fora Collor (15 eventos), com estimativas de público por fonte; complementadas por `data/diretas_ja/` (cronologia de 50 comícios, distribuição estadual dos 490 comícios, atores da coalizão).

### 2.4 Triangulação com bancos independentes (Frente E)

Dois bancos de terceiros incorporados como **fontes independentes** — comparadas, nunca mescladas:

| Banco | Cobertura | Fonte primária |
|---|---|---|
| **NEPAC/UNICAMP** (Tatagiba & Galvão, 2019) | 1.284 eventos, 2011–2016 | Acervo Folha |
| **Mass Mobilization** (Clark & Regan, v16) | 224 protestos no Brasil, 1990–2020 | imprensa internacional (Lexis-Nexis) |

A triangulação (produtos em `data/analise-triangulacao/`) testa as fronteiras de fase do `cycle_phases` contra as séries temporais de eventos e mapeia convergências/divergências entre fontes (crosswalk de categorias em `data/bancos-externos/`).

---

## 3. Hipóteses

O quadro completo — com variáveis independentes/dependentes, indicadores e evidências-âncora — está em [`docs/quadro-hipoteses.md`](docs/quadro-hipoteses.md). São **14 hipóteses em três famílias**:

### Família H1 — Dimensão político-institucional (EOP)

| | Hipótese | Evidência-âncora |
|---|---|---|
| **H1.1** | Quanto maior a abertura do sistema político, maior a probabilidade de mobilizações multisetoriais | Fora Collor: abertura pós-CF88 |
| **H1.2** | Quanto maior a vulnerabilidade das elites governantes, maior a probabilidade de resultado institucional (com DOS como moderadora) | Collor: aprovação 71%→9%; Dilma: crise + Lava Jato + deserção do PMDB |
| **H1.3** | Repressão desproporcional, quando visível midiaticamente, expande o ciclo | 13/06/2013: de 5 mil a 1 milhão em uma semana |
| **H1.4** | Aliados intrainstitucionais ampliam a EOP e a heterogeneidade da coalizão | Fora Dilma: Judiciário, empresariado, mídia; Fora Collor: PT, CUT, Igreja |

### Família H2 — Dimensão discursivo-cultural (DOS)

| | Hipótese | Evidência-âncora |
|---|---|---|
| **H2.1** | O campo que controla a DOS hegemônica direciona o ciclo em favor de sua agenda | Impeachment: DOS antipetista hegemonizada |
| **H2.2** | DOS fragmentada (sem *master frame*) → alta mobilização, baixo resultado definido | Junho 2013: ciclo "inacabado" |
| **H2.3** | Frames culturalmente ressonantes recrutam mais amplamente | Fora Collor: "ética na política" e o ethos de 1988 |
| **H2.4** | A DOS pode ser construída deliberadamente antes da abertura da EOP | Think tanks e mídia, 2013–2014, antes de 2015 |
| **H2.5** | Novas *feeling rules* legitimam emoções políticas e abrem DOS | 2013: a raiva tornada emoção política legítima |

### Família H3 — Integração EOP + DOS + Conjuntura

| | Hipótese | Evidência-âncora |
|---|---|---|
| **H3.1** | Convergência simultânea EOP aberta + DOS convergente maximiza escala e resultado | Padrões: Collor (convergente), 2013 (fragmentado), Dilma (construído) |
| **H3.2** | A capacidade de leitura conjuntural dos atores é variável independente da eficácia estratégica | MBL/VPR leram corretamente; a esquerda, tardiamente |
| **H3.3** | Conjunturas críticas = abertura **simultânea** de EOP e fluidez de DOS | 13/06/2013 como evento-catalisador bifuncional |
| **H3.4** | Assimetria de DOS produz polarização como legado do ciclo | 2013 → frames antipetistas legitimados |
| **H3.5** | Legados institucionais e discursivos de um ciclo condicionam EOP e DOS do seguinte | Refluxo de 2013 pré-moldou 2015–2016 |

---

## 4. Organização do repositório

| Caminho | Conteúdo |
|---|---|
| `artigo/` | Seções redigidas do artigo (introdução, DOS, metodologia, estudo de caso 4.1–4.6, discussão) + referências ABNT (~94) |
| `codebook/` | Codebook do `cycle_phases` (fases, variáveis 0–3, regras de codificação) |
| `data/cycle_phases.csv` | Dataset central: 24 fases × 9 variáveis (v3; backup v2 preservado) |
| `data/protest_events_seeds/` | Sementes manuais: Diretas Já (59) e Fora Collor (15) |
| `data/diretas_ja/` | Cronologia de comícios, distribuição estadual, atores da coalizão |
| `data/bancos-externos/` | NEPAC e Mass Mobilization + crosswalk de códigos |
| `data/analise-triangulacao/` | Produtos da Frente E (triangulação) |
| `docs/` | Projeto, quadro de hipóteses, periodização, protocolo AEP-BEP, incorporação de artefatos |
| `metodologia/` | Relatório metodológico acadêmico (documento vivo) |
| `pipeline/` | Pipeline AEP: scraper Acervo Folha, codificador DoCA, builder, kappa |
| `literature/`, `experiments/` | Levantamento bibliográfico e memorandos exploratórios |
| `research-state.yaml`, `research-log.md` | Estado do projeto e changelog da pesquisa |

## 5. Frentes de trabalho

| Frente | Objetivo | Status |
|---|---|---|
| **C** | Consolidação do artigo em preprint (diagrama EOP–DOS–Conjuntura, abstract, revisão ABNT) | aberta |
| **D** | Execução do pipeline AEP (Acervo Folha) | aguarda credenciais |
| **E** | Triangulação NEPAC × Mass Mobilization × `cycle_phases` | **em curso (prioritária)** |

---

## Referências principais

ALONSO, A. et al. Análise de Eventos de Protesto: decisões metodológicas na organização do BEP 2013-2016. *Plural*, v. 31, n. 2, 2024. · BEACH, D.; PEDERSEN, R. B. *Process-Tracing Methods*. Michigan, 2013. · COSTA, G. P. *Estruturas de mobilização e oportunidades políticas: análise dos ciclos de protestos no Brasil contemporâneo*. Tese (Doutorado) — UFJF, 2024. · DELLA PORTA, D. Protests as critical junctures. *Social Movement Studies*, 2018. · DOBRY, M. *Sociologie des crises politiques*. Paris, 1986. · FERREE, M. M. Resonance and radicalism. *AJS*, 2003. · KOOPMANS, R.; STATHAM, P. Ethnic and civic conceptions of nationhood… 1999. · McADAM, D.; TARROW, S. Ballots and Barricades. *Perspectives on Politics*, 2011. · MISCHE, A. *Partisan Publics*. Princeton, 2008. · TARROW, S. *Power in Movement*. Cambridge, 1994. · TATAGIBA, L. Entre as ruas e as instituições. *Lusotopie*, 2018.

Lista completa (~94 referências, formato ABNT): [`artigo/referencias-abnt.md`](artigo/referencias-abnt.md).
