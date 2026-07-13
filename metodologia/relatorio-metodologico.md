# Relatório Metodológico

**Projeto:** Ciclos de Protesto no Brasil — Estruturas de Oportunidades Políticas (EOP),
Estruturas de Oportunidades Discursivas (DOS) e Análise de Conjuntura
**Pesquisador responsável:** Gustavo Paccelli Costa (Tese de Doutorado, UFJF, 2024, como fonte primária)
**Documento:** descrição metodológica das etapas de produção da pesquisa
**Última atualização:** 2026-07-04

---

## Sumário

1. Apresentação e objeto
2. Abordagem teórico-metodológica
3. Desenho de pesquisa e periodização
4. Prospecção e coleta de dados
   - 4.1 Pipeline de Análise de Eventos de Protesto (AEP) — Acervo Folha
   - 4.2 Protocolo de codificação (DoCA / BEP-CEBRAP / MPEDS)
   - 4.3 Bancos de dados de terceiros incorporados
   - 4.4 Sementes de dados próprios
   - 4.5 Validação de cronologia e fontes
5. Organização e governança do repositório
6. Insights produzidos
7. Limitações e agenda
8. Cronologia das etapas executadas

---

## 1. Apresentação e objeto

Esta pesquisa investiga **como as configurações de estruturas de oportunidades políticas (EOP) e
discursivas (DOS), lidas conjunturalmente pelos atores, condicionam a emergência, a dinâmica de
fases e os desfechos dos ciclos de protesto no Brasil**. O recorte empírico abrange quatro ciclos
canônicos da trajetória de redemocratização: **Diretas Já (1983–1985), Fora Collor (1991–1992),
Junho de 2013 e Impeachment de Dilma Rousseff (2014–2016)**.

O projeto é uma agenda pós-defesa que consolida e dá continuidade à tese de doutorado do
pesquisador, mobilizando-a como fonte empírica primária e articulando-a a um quadro teórico
integrado — o *triângulo* EOP–DOS–Análise de Conjuntura — e a uma infraestrutura de dados
quantitativa e qualitativa.

---

## 2. Abordagem teórico-metodológica

### 2.1 Filiação teórica

A pesquisa filia-se à **Teoria do Processo Político / Confronto Político** (McAdam, Tarrow &
Tilly, 2001; Tarrow, 2011; Tilly, 2006), articulada a três vertentes complementares:

- **Estruturas de Oportunidades Políticas (EOP)** — abertura institucional, divisão de elites,
  aliados influentes, crise de legitimidade e repressão (Tarrow, 2011; McAdam, 1982; Kriesi et
  al., 1995).
- **Estruturas de Oportunidades Discursivas (DOS)** — visibilidade midiática, ressonância dos
  *frames* e legitimidade narrativa (Koopmans & Statham, 1999; Koopmans & Olzak, 2004; McCammon,
  2013; Snow & Benford, 1988; Benford & Snow, 2000).
- **Tradição brasileira de análise de conjuntura**, ancorada nos conceitos de **conjunturas
  críticas** (della Porta, 2018, 2022; Mariano, Ferreira & Neves, 2023) e **conjunturas fluidas**
  (Dobry, 1986).

A contribuição original do projeto é a **integração desses três vértices** em um quadro único,
capaz de distinguir, no interior de uma mesma conjuntura, as condições político-institucionais
(EOP), simbólico-discursivas (DOS) e a capacidade de leitura conjuntural dos atores.

### 2.2 Estratégia metodológica

A estratégia central é a **comparação qualitativa estruturada e focada** de casos históricos,
complementada por:

- **Codificação ordinal** das fases dos ciclos (dataset `cycle_phases`), permitindo comparação
  sistemática 4×N em escala 0–3;
- **Process tracing analítico** (Beach & Pedersen, 2013; Mahoney, 2001), de orientação
  mecanicista e configuracional (dada a inviabilidade de estimar efeitos médios com N=4 casos e
  forte suspeita de equifinalidade);
- **Análise de Eventos de Protesto (AEP/PEA)** no nível do evento, ancorada no Protocolo
  BEP-CEBRAP (Alonso et al., 2024) e na infraestrutura MPEDS (Hanna, 2017).

A comparação combina lógicas *most similar* (todos os ciclos são mobilizações multissetoriais de
grande escala em torno de crises presidenciais) e *most different* (variação em EOP, DOS,
estruturas de mobilização e perfil ideológico dos atores), com as **Diretas Já** como caso de
fronteira, por ocorrerem sob regime autoritário em liberalização.

---

## 3. Desenho de pesquisa e periodização

### 3.1 Unidade de análise e variáveis

O dataset **`cycle_phases`** (`data/cycle_phases.csv`) tem como unidade a **fase de ciclo**
(cycle × phase) e codifica **9 variáveis** em escala ordinal 0–3:

| Bloco | Variáveis |
|---|---|
| Oportunidades Políticas (EOP) | abertura institucional; divisão de elites; aliados influentes; crise de legitimidade; repressão |
| Tradução institucional | grau em que o resultado é obtido por canal institucional distinto do demandado |
| Oportunidades Discursivas (DOS) | visibilidade midiática; ressonância discursiva; legitimidade narrativa |

### 3.2 Periodização em fases (v3, 24 fases)

Cada ciclo é decomposto em fases. Além das fases canônicas (emergência, expansão, pico, declínio,
desfecho), o desenho incorpora **três fases não-canônicas**, teoricamente fundamentadas:

- **Articulação** — construção prévia de estruturas de mobilização e oportunidades antes da fase
  pública contenciosa. Presente em Diretas Já (1982–83), Fora Collor (nov/1991–mai/1992; Mische,
  2008) e Impeachment Dilma (out/2014–mar/2015; mobilização eleitoral reativa pós-derrota de
  Aécio Neves — McAdam & Tarrow, 2011; Tatagiba, 2018). **Ausente** em Junho de 2013, cuja
  pré-história (Revolta do Buzu, 2003; fundação do MPL-Brasil no FSM, 2005) é esporádica: o ciclo
  irrompe por ruptura de amplitude, não por articulação deliberada.
- **Radicalização** — específica de Junho de 2013 (21/06–31/07): após a violência policial contra
  manifestantes (13/06) e o confronto com *black blocs* (17/06), e após o pico (20/06) com a
  retirada do MPL (21/06), o repertório radicaliza e a DOS se inverte pela segunda vez.
- **Latência** — vale de mobilização entre expansão e pico (ciclo Dilma: ago–dez/2015).

A fronteira **Junho 2013 → Impeachment Dilma** foi redefinida: Junho encerra-se em 2013 (ciclo de
eclosão); a articulação do impeachment inicia-se após o 2º turno de 26/10/2014. A periodização é
documentada e versionada (`docs/periodizacao-articulacao.md`, `docs/periodizacao-revisao.md`),
com preservação das versões anteriores (`data/cycle_phases_v2_prearticulacao.csv`).

### 3.3 Quadro de hipóteses

O desenho é orientado por **14 hipóteses em 3 famílias** (`docs/quadro-hipoteses.md`):
H1 (político-institucional), H2 (discursiva) e H3 (modelo integrado). Cada hipótese especifica
variável independente, dependente, indicadores e evidência-âncora.

---

## 4. Prospecção e coleta de dados

A estratégia de dados é **triangular**: combina (a) um pipeline próprio de AEP a construir sobre o
Acervo Folha; (b) bancos de dados acadêmicos de terceiros; (c) sementes de dados codificadas
manualmente; e (d) a validação sistemática de cronologia e fontes. As fontes são tratadas como
**independentes e não somáveis** — o uso conjunto é de corroboração e triangulação, nunca de
agregação direta.

### 4.1 Pipeline de Análise de Eventos de Protesto (AEP) — Acervo Folha

Foi projetado um pipeline em quatro passos (`pipeline/`) para a construção do banco
`protest_events` a partir do **Acervo Folha de S.Paulo**:

1. **`01_scraper.py`** — raspagem via **Playwright** (navegador headless Chromium). Realiza login
   no Acervo, itera termos de busca × janelas temporais definidas em `config/queries.yaml`, salva
   cada artigo como JSON e mantém **estado incremental** (permite interromper e retomar). Os
   seletores CSS são centralizados para manutenção, dado que o Acervo é uma aplicação dinâmica
   (React) sujeita a mudanças de layout.
2. **`02_doca_coder.py`** — codificação assistida por IA via **API Anthropic** com *structured
   outputs* (JSON validado por esquema), *prompt caching* do system prompt e **UUID5
   determinístico** por evento (deduplicação estável). Aplica os critérios de elegibilidade e o
   codebook.
3. **`03_build_dataset.py`** — normalização contra os dicionários do codebook, *clustering* para
   evento canônico (deduplicação entre fontes) e exportação CSV/XLSX multi-aba.
4. **`04_intercoder_reliability.py`** — aferição de confiabilidade inter-codificadores por
   **Cohen's Kappa** (limiar ≥ 0,75; Krippendorff, 2004).

**Organização do scrap.** A busca replica o protocolo BEP: palavras-chave validadas
(`manifestação`, `protesto`, `passeata`, `greve`, `ocupação`, etc.), janelas temporais por ciclo
mais uma varredura geral, e triagem editorial em duas passagens (título → leitura integral) com
supervisão humana amostral. O fluxo é descrito em `docs/aep-protocol-bep.md` (§§ 3, 10, 11) como
um **workflow multi-passagem** (artigo → evento → evento canônico → adjudicação).

**Estado atual.** O pipeline está estruturalmente completo, porém **não executado**: depende de
(i) validação dos seletores contra o site logado, (ii) instalação de dependências e configuração
de credenciais em `.env` (nunca versionado), e (iii) primeira execução de teste com aferição de
Kappa. A execução está em pausa por decisão do pesquisador.

### 4.2 Protocolo de codificação (DoCA / BEP-CEBRAP / MPEDS)

O codebook do banco de eventos (`pipeline/config/doca_codebook.yaml`) integra três referências:

- **Protocolo BEP-CEBRAP** (Alonso et al., 2024) — âncora metodológica central: definição
  operacional de evento de protesto (4 critérios de inclusão + exclusões), critérios de
  continuidade espaço-temporal (evento ≠ notícia), e **5 blocos de variáveis** (identificação,
  atores, performances, temas/slogans, respostas das autoridades).
- **MPEDS** (Hanna, 2017) — infraestrutura de AEP automatizada: conceito de **evento canônico**
  (deduplicação entre fontes), *flag* de artigo com múltiplos eventos, e campos de deduplicação e
  contexto (`canonical_event_id`, `end_date`, `duration_days`, `counter_protest`, `smo`,
  `target`).
- **Valências** (do codebook DoCA original) — posição do protesto em relação à demanda
  (pró/anti/indeterminado).

O sistema de códigos de demanda (`claim_codes`) organiza-se em 9 domínios temáticos de quatro
dígitos; os repertórios seguem os verbos canônicos de Tilly/BEP.

### 4.3 Bancos de dados de terceiros incorporados

Foram incorporados dois bancos acadêmicos, mantidos como **fontes independentes** em
`data/bancos-externos/`, cada qual com fonte original preservada, dados em CSV e livro de código:

| Banco | Autoria | Cobertura | Unidade | N (Brasil) |
|---|---|---|---|---|
| **NEPAC** | Tatagiba & Galvão (UNICAMP, 2019) | 2011–2016 | cidade-evento | 2.548 registros / 1.284 eventos |
| **Mass Mobilization** | Clark & Regan (v16, 2020) | 1990–2020 | protesto–país–ano | 224 protestos (ccode 140) |

O banco NEPAC (fonte: Acervo Folha) oferece microdados nacionais densos para 2011–2016; o Mass
Mobilization (fonte: imprensa internacional/Lexis-Nexis) oferece a série temporal mais longa
(alcança o Fora Collor) e a dimensão comparada internacional. Um **crosswalk** documentado
(`data/bancos-externos/mass-mobilization-clark-regan-2020/livro-codigo/crosswalk-codigos.md`)
relaciona — **sem mesclar** — as categorias do MM aos códigos DoCA/BEP e NEPAC, explicitando as
diferenças metodológicas (limiares de inclusão, fontes e definições de alvo) que tornam as bases
não somáveis.

### 4.4 Sementes de dados próprios

Para os ciclos **pré-2011**, não cobertos adequadamente pelos bancos externos, foram incorporadas
**sementes de `protest_events`** codificadas manualmente (`data/protest_events_seeds/`): **59
eventos das Diretas Já** e **15 do Fora Collor**, com múltiplas estimativas de público por fonte
(mín/máx/mediana) e fonte primária. Alimentam diretamente o banco a ser expandido pelo pipeline.

### 4.5 Validação de cronologia e fontes

As datas-chave dos quatro ciclos foram **validadas** (`docs/cronologia-validada.md`) com
substituição de fontes de baixo prestígio (Terra, Wikipédia, Politize) por fontes institucionais
e jornalísticas de referência (Agência Brasil/EBC, Portal da Câmara, Senado Federal, CPDOC/FGV,
Fundação Perseu Abramo). Discrepâncias foram corrigidas — notadamente o comício de Goiânia das
Diretas, reposicionado de "fevereiro/1984" para **12 de abril de 1984**. Registrou-se a
divergência sistemática entre estimativas de público (PM vs. Datafolha), tratada por faixas.

---

## 5. Organização e governança do repositório

O projeto é versionado em Git (repositório `gustavopaccelli/research`). Adotaram-se práticas de
governança de dados e rastreabilidade:

- **Rastreamento central:** `research-state.yaml` (estado dos componentes e frentes),
  `research-log.md` (linha do tempo de decisões), `docs/tarefas.md` (inventário de tarefas).
- **Preservação de fontes:** arquivos originais (`.docx`, `.xlsx`, `.pdf`) mantidos sem alteração;
  conversões (para CSV/Markdown, datas ISO) documentadas; nenhuma imputação silenciosa.
- **Incorporação de artefatos:** os produtos das sessões de trabalho do pesquisador (pasta
  `artefatos/`) foram revistos item a item, com parecer explícito de incorporação, superação ou
  reserva (`docs/artefatos-incorporacao.md`).
- **Segurança:** credenciais (`.env`) nunca versionadas; verificação sistemática da ausência de
  segredos nos commits.
- **Bibliografia:** `artigo/referencias-abnt.md` reúne ~90 referências em norma ABNT, com
  verificação de fontes e marcação de itens a confirmar.

---

## 6. Insights produzidos

A articulação teórico-empírica produziu um conjunto de achados analíticos, consolidados no artigo
(`artigo/secoes/`) e no quadro de hipóteses:

1. **Quatro padrões de articulação EOP+DOS.** (i) *Convergência* (Fora Collor) → mobilização
   massiva com desfecho previsível; (ii) *abertura caótica* (Junho 2013) → alta mobilização sem
   resultado institucional definido; (iii) *construção deliberada* (Impeachment) → desfecho
   definido por atores estratégicos; (iv) *assimetria DOS* → polarização e disputa de legitimidade.

2. **DOS explica emergência/escala; divisão de elites explica desfecho institucional.** O
   alinhamento estável das duas dimensões produz ciclos curtos e canalizados; sua abertura
   descoordenada produz ciclos longos e inconclusos.

3. **Mídia como *gatekeeper* vs. produtora ativa de frames.** Nas Diretas Já a grande mídia
   operou como *gatekeeper* de visibilidade (bloqueio tardio); no Fora Collor e no Impeachment,
   como produtora ativa de frames. Distinção que refina o conceito de DOS.

4. **Endogeneidade das oportunidades.** Os ciclos não apenas exploram, mas *aprofundam* as
   divisões de elite que os favorecem (evidente nas Diretas e no Fora Collor).

5. **Tradução institucional como variável.** O desfecho pode ser obtido por canal institucional
   distinto do demandado (Diretas Já perde a emenda mas elege Tancredo) — capturado pela variável
   `traducao_institucional`.

6. **Deslocamento do *master frame*.** Da democratização (1984) à ética/anticorrupção (1992 em
   diante), com a inclusão das Diretas Já permitindo observar essa trajetória de longo prazo.

7. **Articulação como fase heurística.** A distinção entre ciclos com articulação prévia (Collor,
   Dilma) e ciclos por ruptura (Junho 2013) fundamenta empiricamente a fronteira entre ciclos e a
   relação recíproca entre eleições e movimentos (confronto eleitoral).

---

## 7. Limitações e agenda

- **Execução do pipeline** pendente de credenciais e validação de seletores (Frente D, em pausa).
- **Scores das fases de articulação** e valores de `traducao_institucional` foram derivados
  analiticamente (a partir das versões dos artefatos e da tese) e comportam revisão do pesquisador.
- **Não coleta de dados primários originais**: as interpretações ancoram-se em fontes secundárias
  sistematizadas; a contribuição é conceitual e metodológica.
- **Agenda:** consolidação do artigo em preprint (Frente C); análise de triangulação dos bancos e
  sementes (Frente E); execução do pipeline (Frente D).

---

## 8. Cronologia das etapas executadas

| Período | Etapa |
|---|---|
| 2026-04 a 06 | Formulação da pergunta; desenho do triângulo EOP–DOS–Conjuntura; codebook `cycle_phases`; 14 hipóteses; tese como fonte primária |
| 2026-06-10 | Consolidação no repositório; periodização v2 validada; reconstrução do pipeline PEA |
| 2026-06-16 | Incorporação do Protocolo BEP-CEBRAP (Alonso et al., 2024); quadro de hipóteses |
| 2026-07-03 | Enriquecimento bibliográfico; validação da cronologia; integração MPEDS |
| 2026-07-04 | Inclusão das Diretas Já no estudo de caso (4 ciclos); incorporação dos bancos NEPAC e Mass Mobilization; incorporação da pasta `artefatos/` (sementes, referências, valências); periodização v3 (fases de articulação, latência, `traducao_institucional`) fundamentada na tese |

---

*Documento vivo — atualizar a cada nova etapa metodológica relevante. Referências completas em
`artigo/referencias-abnt.md`.*
