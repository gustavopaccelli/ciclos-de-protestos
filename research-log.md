# Research Log — Linha do Tempo de Decisões

## 2026-06-10 — Bootstrap
- Pergunta de pesquisa definida com o usuário: EOP + oportunidades discursivas em
  4 ciclos de protesto brasileiros (Diretas Já, Fora Collor, Junho 2013, impeachment Dilma).
- Workspace inicializado (research-state.yaml, findings.md, literature/, experiments/).
- Levantamento bibliográfico inicial: núcleo teórico (Tarrow, McAdam, Koopmans &
  Statham, Koopmans & Olzak, McCammon) + literatura dos casos (Alonso & Mische 2017,
  Tatagiba 2014, Sallum Jr. 2015, Singer 2013, Avritzer 2016/2017).
- Lacuna identificada: comparação sistemática dos 4 ciclos sob grade conjunta EOP+DOS.
- Hipóteses H1–H4 formuladas (ver research-state.yaml).
- Decisão metodológica: comparação qualitativa estruturada e focada (George & Bennett),
  com matriz analítica comum às 4 dimensões de EOP e 3 de DOS por caso.
- Limitações de infraestrutura registradas: sem Semantic Scholar/Consensus; verificação
  bibliográfica via WebSearch.
- Próximo passo: análise de caso C1 (Diretas Já) com a matriz EOP+DOS
  (experiments/c1-diretas-ja/).

## 2026-06-10 — Inner loop 1: C1 Diretas Já
- Análise C1 concluída (experiments/c1-diretas-ja/analysis.md).
- P1 (H1) suportada; P3 (H4) suportada; P2 (H2) parcialmente suportada — em 1984
  a mídia foi gatekeeper tardio, não produtora de frames; H2 será refinada.
- Achados exploratórios: endogeneidade das oportunidades (E1); distinção
  demanda atendida vs. realinhamento produzido na variável desfecho (E2).
- Próximo: protocolo e análise C2 (Fora Collor).

## 2026-06-10 — Inner loop 2: C2 Fora Collor
- Análise C2 concluída; P1–P4 todas suportadas.
- Contraste-chave com C1: ordem causal invertida (divisão de elite PRECEDE o ciclo
  em 1992; em 1984 o ciclo aprofunda a divisão) e mídia como produtora ativa de
  frames (vs. gatekeeper tardio em 1984).
- Exploratórios: E3 (via institucional disponível encurta o ciclo — candidata a H4.1);
  E4 (DOS como terreno de disputa simbólica).
- Próximo: protocolo e análise C3 (Junho de 2013).

## 2026-06-10 — Inner loop 3: C3 Junho 2013 (caso desviante)
- H1 REFUTADA como enunciada: 2013 emerge sem divisão de elite. Reformulação:
  divisão de elite é condição do desfecho institucional, não da emergência.
- P2–P4 suportadas. Exploratórios: E5 (repressão abre a DOS); E6 (ciclos como
  série conectada — desfecho de 2013 é insumo de 2015-16).
- Próximo: protocolo e análise C4 (impeachment Dilma); depois outer loop 1.

## 2026-06-10 — Inner loop 4: C4 impeachment Dilma + Outer loop 1
- C4: P1–P4 suportadas (com H1 reformulada). Exploratórios: E7 (contra-ciclo
  disputando a DOS), E8 (oportunidades judiciais — Lava Jato).
- Outer loop 1 (DEEPEN): tese central formulada — DOS explica emergência/escala,
  divisão de elite explica desfecho institucional; alinhamento estável das duas
  produz ciclos curtos e canalizados. Quadro comparativo 4 casos em findings.md.
- Pendências antes de CONCLUDE: survey de legal opportunity structure; verificação
  de citações de memória; fichamento de Tatagiba 2014.

## 2026-06-10 — Outer loop 2: PIVOT para o desenho consolidado do projeto
- Usuário trouxe 4 documentos das sessões claude.ai (abr–jun/2026) com o estado
  real do projeto: artigo do triângulo EOP–DOS–Análise de Conjuntura (seções
  redigidas), codebook cycle_phases (8 variáveis, 0–3, 5 fases), scores dos 4
  ciclos validados em 2026-06-05, quadro de 14 hipóteses (3 famílias) e pipeline
  PEA do Acervo Folha.
- Repositório reorganizado: codebook/ (codebook YAML), data/cycle_phases.csv
  (scores formalizados), artigo/secoes/ (textos extraídos dos documentos),
  artigo/referencias-abnt.md, docs/projeto.md (visão geral e frentes abertas).
- Framework bootstrap da sessão rebaixado a material exploratório
  (experiments/README.md).
- Pendências de incorporação: .docx do quadro de 14 hipóteses; nota
  teórico-metodológica .docx; cycle_phases.xlsx original; ZIP da pipeline.
- Próximas frentes: (B) refinamento da periodização; (C) inferência causal /
  teste de H1.2; (D) pipeline protest_events.

## 2026-06-10 — Frente D: pipeline protest_events reconstruída
- pipeline/ criada: 01_scraper.py (Playwright/Acervo Folha, incremental),
  02_doca_coder.py (API Anthropic: structured outputs + prompt caching +
  UUID5 determinístico), 03_build_dataset.py (dedupe, CSV/XLSX 4 abas),
  04_intercoder_reliability.py (Cohen's Kappa), run_pipeline.py, configs
  (queries.yaml; doca_codebook.yaml RECONSTRUÍDO — validar contra o original)
  e docs/TUTORIAL.md.
- Execução pendente de credenciais do Acervo Folha e ANTHROPIC_API_KEY (.env).

## 2026-06-10 — Frente B: revisão da periodização (PROPOSTA)
- docs/periodizacao-revisao.md + data/cycle_phases_v2_proposta.csv (v1 intacta).
- J13: fase RADICALIZAÇÃO (21/06–31/07) inserida entre pico (encurtado p/
  18–20/06) e declínio (ago–out, cobrindo cauda da greve dos professores/RJ);
  captura a 2ª inversão da DOS (recriminalização) — reforça padrão 2 e H2.2.
- Impeachment: expansão estendida até 30/11/15 (TCU 02/10, pauta-bomba,
  articulação Temer = construção institucional da janela); pico estendido até
  11/05/16 (tramitação no Senado); início em 26/10/14 validado (padrão 3 —
  construção deliberada exige incluir a fase formativa).
- Aguardando validação do usuário para substituir a v1.

## 2026-06-10 — Frente B VALIDADA pelo usuário
- v2 adotada integralmente: data/cycle_phases.csv substituído (21 fases);
  codebook atualizado com a fase radicalizacao e a nota de periodização.
- Pendência menor: conferir datas dos comícios de abr/1984 e dos atos de
  out/2013 na redação final.

## 2026-06-10 — Frente C em espera
- Usuário validou a periodização v2 integralmente, mas pediu para NÃO iniciar
  a inferência causal por enquanto — está reavaliando a abordagem. Aguardar
  decisão antes de qualquer trabalho na frente C.

## 2026-06-16 — Incorporação do Protocolo BEP-CEBRAP (Alonso et al. 2024)

**Artigo incorporado:** Alonso, A.; Rezende, P. J.; Souza, R. de; Souza, V. B. de.
"Análise de Eventos de Protesto: decisões metodológicas na organização do Banco de
Eventos de Protesto (BEP) 2013-2016." *Plural*, v. 31.2, 2024, p. 288-323.
DOI: 10.11606/issn.2176-8099.pcso.2024.233335

**Aplicabilidades metodológicas (Frente D — pipeline protest_events):**
- Definição operacional de evento de protesto formalizada: 4 critérios de inclusão
  (ação pública coletiva / não estatal / contestatória / com reivindicações) e
  exclusões explícitas (individual, lúdico, rotineiro, virtual, não-confirmado).
- Critérios de continuidade espaço-temporal para delimitação da unidade analítica
  (evento ≠ notícia): regra das 24h; continuidade espacial; separação por pautas opostas.
- Validação das palavras-chave do `queries.yaml` (conjunto testado pelo BEP em 17.752
  notícias de Junho 2013).
- Estratégia de fonte primária (Folha de S.Paulo) + secundária (G1/portais regionais)
  para controle dos vieses de seleção e descrição.
- 5 blocos de variáveis BEP mapeados para o `event_schema` do codebook DoCA; novos
  campos incorporados: `location_venue_type`, `location_conventional`, `city_size`,
  `crowd_size_bep`, `actor_org_type`, `actor_formalization`, `action_object`,
  `action_instrument`, `symbols`, `slogans`, `conflict_inter_group`.
- Verbos canônicos de ação (dicionário BEP) incorporados ao `repertoires`.
- Limiar de confiabilidade inter-codificadores: Cohen's Kappa ≥ 0,75.
- Threshold de exclusão para variáveis com excesso de missings: >30%.
- Legitimidade metodológica explicitada pelos autores para uso de IA/NLP em
  codificação semi-automática — desde que ancorada em bom desenho de pesquisa.

**Contribuições epistemológico-teóricas (projeto geral):**
- Neutralidade axiológica da AEP: banco captura tanto ciclos progressistas quanto
  conservadores — essencial para o desenho comparativo dos 4 ciclos do projeto.
- Filiação à TCP (McAdam, Tarrow, Tilly): confirma coerência teórica entre o quadro
  EOP+DOS do projeto e o método empírico da AEP.
- Articulação sintaxe (Franzosi: ator–ação–objeto) + semântica (Benford & Snow: frames)
  — mapeia diretamente para EOP (estrutural) e DOS (discursiva).
- Bloco V (respostas das autoridades): codifica a dimensão repressiva — variável
  central para teste de H1 (efeito da repressão sobre escala e resultado do ciclo).

**Arquivos criados/modificados:**
- `docs/aep-protocol-bep.md` — memo metodológico canônico (CRIADO)
- `pipeline/config/doca_codebook.yaml` — alinhado ao BEP (5 blocos, novos campos)
- `docs/projeto.md` — referência a Alonso et al. e aep-protocol-bep.md adicionada
- `research-state.yaml` — método e Frente D atualizados

## 2026-07-03 — Consolidação: bibliografia, cronologia validada, integração MPEDS

### Tarefa 1 — Enriquecimento bibliográfico (concluída)
- `artigo/referencias-abnt.md` expandido de 34 para 64 entradas, adicionando:
  - Núcleo teórico AEP/PEA: Earl et al. (2004), Fillieule & Jiménez (2003), Franzosi (2004),
    Hanna (2017/MPEDS), Goodwin & Jasper (1999).
  - Núcleo TCP completo: McAdam (1982), McAdam, Tarrow & Tilly (2001), Kriesi et al. (1995),
    Snow & Benford (1988; 1992), Tilly (1978; 2006), Tilly & Tarrow (2015), Tarrow (2011).
  - Casos brasileiros: Mische (2008), Saad-Filho (2013), Solano (2018), Tatagiba (2014),
    Weyland (1993), Kotscho (1984), Rodrigues A. T. (2003), Alonso (2015).
  - Infraestrutura: MPEDS (Hanna 2017), Vandenberghe (2025).

### Tarefa 2 — Validação da cronologia (concluída)
- **Fonte eliminada:** Terra.com.br substituído por Agência Brasil/EBC, Portal da Câmara,
  Senado Federal, CPDOC/FGV e Fundação Perseu Abramo.
- **Discrepância corrigida:** Comício de Goiânia (Diretas Já) era registrado como
  "fevereiro de 1984" — confirmado como **12 de abril de 1984** (Praça Cívica, ~300 mil).
- `docs/cronologia-validada.md` criado com tabela completa de datas-chave, público estimado
  e fonte confirmadora para os 4 ciclos.
- `data/cycle_phases.csv` não requer correção: a data de Goiânia não consta como data
  explícita nas fases (fase DJ-3 cobre abr/1984 — compatível com a data corrigida).

### Tarefa 3 — Integração MPEDS (concluída)
- `pipeline/config/doca_codebook.yaml` — novos campos incorporados ao `event_schema`:
  `end_date`, `duration_days`, `multi_event_article`, `canonical_event_id`, `article_desc`,
  `event_desc`, `counter_protest`, `smo`, `target`. Novas seções: `mpeds_form_categories`
  (mapeamento 11 formas MPEDS → verbos BEP) e `mpeds_target_categories` (7 alvos adaptados
  para o Brasil).
- `docs/aep-protocol-bep.md` — adicionadas §10 (evento canônico e deduplicação) e §11
  (workflow multi-passagem: 5 passagens sequenciais scraper → triagem → codificação →
  dataset → confiabilidade).
- `literature/survey.md` — adicionadas seção §4 (AEP/PEA Metodologia) e §5
  (Infraestrutura computacional — MPEDS e afins).
- Classificadores ML do MPEDS (inglês) e interface Flask NÃO incorporados — substituídos
  pelo LLM DoCA/Anthropic do pipeline existente.

**Nota:** Frente C redefinida pelo usuário (2026-07-03): deixa de ser "estratégia
de inferência causal" e passa a ser "consolidação do artigo para preprint",
incluindo integração do quadro de 14 hipóteses como seção de discussão.

## 2026-07-04 — Frente C: alinhamento do artigo a 4 ciclos (inclusão das Diretas Já)

**Decisão do usuário:** o estudo de caso do artigo cobria apenas 3 ciclos (Fora
Collor, Junho 2013, Impeachment), enquanto o dataset/hipóteses/cronologia cobrem
4. Optou-se por INCLUIR Diretas Já no artigo, alinhando-o à grade completa.

**Alterações no artigo (`artigo/secoes/`):**
- `04b-estudo-de-caso.md` — nova subseção empírica 4.2 "A campanha das Diretas Já
  (1983–1984): EOP de transição, DOS de ressonância máxima e mídia como gatekeeper";
  demais subseções renumeradas (Collor 4.3, Junho 2013 4.4, Impeachment 4.5,
  síntese 4.6). Título atualizado (1992–2016 → 1984–2016). Apresentação (4.1) e
  primeiro padrão da síntese reescritos para integrar Diretas Já; incorporada a
  distinção mídia gatekeeper vs. produtora de frames e a tese da endogeneidade
  das oportunidades (ciclo aprofunda a divisão de elite que o favorece).
- `04a-introducao-estudo-caso.md` — passa de "três" para "quatro ciclos"; Diretas
  Já como caso de origem da gramática contenciosa e do deslocamento do master frame.
- `03-metodologia.md` — comparação estendida a 4 ciclos; Diretas Já como caso de
  fronteira (regime autoritário em liberalização vs. democracia consolidada);
  fontes das Diretas Já (Rodrigues 2003, Leonelli & Oliveira 2004, Bertoncelo 2007,
  Markun 2014).
- `05-discussao-conclusiva.md` — "quatro ciclos"; Diretas Já como exemplo inaugural
  de leitura conjuntural acurada.

**Base empírica da subseção:** experiments/c1-diretas-ja/analysis.md (matrizes
EOP/DOS, teste de predições) + docs/cronologia-validada.md (datas e placares).

**Pendências da Frente C:** consolidar seções em documento único; figura do
triângulo; abstract e palavras-chave; revisão final ABNT ao periódico-alvo.

## 2026-07-04 — Incorporação do banco NEPAC/UNICAMP (Tatagiba & Galvão 2019)

**Solicitação do usuário:** incorporar o banco de protestos 2011-2016 (NEPAC/UNICAMP,
https://nepac.ifch.unicamp.br/banco-de-dados) e criar pasta organizada para bancos.

**Estrutura criada** — `data/bancos-externos/` como raiz para bancos de terceiros,
com padrão por subpasta (fonte-original/ + dados/ + livro-codigo/ + README):
- `data/bancos-externos/README.md` — princípio de organização e regras (preservar
  original, documentar conversões, atribuição, sem credenciais).
- `data/bancos-externos/nepac-tatagiba-galvao-2019/`:
  - `fonte-original/` — xlsx e docx originais preservados sem alteração.
  - `dados/protestos_2011-2016.csv` — XLSX convertido p/ CSV UTF-8; única
    transformação: datas seriais Excel → ISO 8601 (base 1899-12-30). 2.548 registros
    cidade-evento / 1.284 eventos únicos; 27 variáveis.
  - `livro-codigo/livro-de-codigo.md` — livro de código transcrito (definição de
    evento Tilly 1978/Olzak 1989; códigos de base mobilizada; 15 grupos sociais;
    11 categorias de reivindicação).
  - `README.md` — manifesto (proveniência, dicionário de colunas, distribuição por
    ano, relação com o projeto, referência ABNT).

**Distribuição por ano:** 2011=209, 2012=407, 2013=729, 2014=268, 2015=454, 2016=481
(pico em Junho 2013 e alta no ciclo do impeachment — cobre 2 dos 4 ciclos do projeto).

**Relação com o projeto:** microdados evento-a-evento complementares ao cycle_phases
(ordinal fase×ciclo) e ao pipeline AEP. Definição de evento de Tatagiba & Galvão
dialoga com o Protocolo BEP-CEBRAP (Alonso et al. 2024) — ambos usam Folha e evento
como unidade. Base para validação empírica externa de J13 e Impeachment.

## 2026-07-04 — Incorporação do banco Mass Mobilization (Clark & Regan) — só Brasil

**Solicitação do usuário:** incorporar dados do projeto Mass Mobilization (MM),
focando SOMENTE no Brasil, 1990 até a última data; verificar a tabela de códigos e
adaptar aos códigos existentes; NÃO mesclar — tratar como fonte independente.

**Verificação prévia:** MM não estava no repositório (fonte nova).

**Arquivos-fonte:** `MM_users_manual_0515.pdf` (codebook 2015) + `mmALL_073120_csv.csv`
(global, 15 MB) + `mmALL_073120_v16.dta` (29 MB). Arquivo de dados v16 estende a
cobertura de 1990-2014 (manual) para **1990-2020**.

**Recorte:** extraído SOMENTE Brasil (`ccode = 140`), todos os anos → **224 protestos**
(todos protest=1). Arquivos globais (44 MB, 162 países) NÃO versionados — fora do
escopo; extração reprodutível por filtro ccode==140. Manual PDF preservado.

**Estrutura criada** — `data/bancos-externos/mass-mobilization-clark-regan-2020/`:
- `fonte-original/MM_users_manual_0515.pdf` — codebook oficial.
- `dados/protestos_brasil_1990-2020.csv` — 224 registros, 31 colunas, só Brasil.
- `livro-codigo/livro-de-codigo.md` — variáveis + tabelas de código (7 demandas,
  7 respostas estatais, faixas de participação); def. de protesto (≥50 pessoas,
  antiestatal; exclui comícios, intercomunais, rebeldes).
- `livro-codigo/crosswalk-codigos.md` — correspondência conceitual (SEM mesclar)
  entre categorias MM e códigos DoCA/BEP (claim_codes, repression_levels) e NEPAC.

**Distribuição:** picos em 2013, 2015 e 2016 (23 cada). Demanda primária dominante:
political behavior/process (136/224). Resposta estatal dominante: ignore (140/224).

**Princípio metodológico registrado:** MM, NEPAC e pipeline DoCA são fontes
INDEPENDENTES e NÃO somáveis (limiares, fontes primárias e definições de alvo
distintos). Uso conjunto = triangulação (comparar tendências, corroborar picos),
nunca agregação. MM oferece a série mais longa (desde 1990, cobre Fora Collor) e a
dimensão comparada internacional.

## 2026-07-04 — Incorporação da pasta artefatos/ (produtos do Projeto claude.ai)

Revisão completa dos 31 arquivos em artefatos/ (3 subpastas). Parecer detalhado por
arquivo em docs/artefatos-incorporacao.md. Regra: incorporar o que incrementa; ignorar
o defasado; preservar tudo.

**Incorporado:**
- Sementes protest_events → data/protest_events_seeds/ (Diretas Já 59 eventos + Fora
  Collor 15 eventos), com estimativas de público por fonte. Preenchem a lacuna dos
  ciclos pré-2011 que MM/NEPAC não cobrem.
- 14 referências ausentes do referencias_ciclos_protesto.bib → artigo/referencias-abnt.md
  (Piven & Cloward, Entman, Habermas, Dobry, Beach & Pedersen, Davenport, Alexander,
  Hutter, Ortellado/Solano/Moretto, Nunes & Melo, Ansell, Fernandes, Scartezini, Sørbøe).
- Variável `valences` (pró/anti/indeterminado) do codebook DoCA original →
  pipeline/config/doca_codebook.yaml (resolve a pendência "validar codebook contra o
  original": nosso codebook cobre e supera o original, exceto pelas valences, agora incluídas).

**Superado (preservado, não reincorporado):** quadro de hipóteses (já em docs/), pipeline
original (já reconstruído e evoluído com BEP+MPEDS), notas metodológicas antigas.

**Fonte para a Frente C (consolidação do artigo):** EOP_DOS_Conjuntura_Artigo_Completo_v1,
artigo_H12_vulnerabilidade_elites, artigo_processo_politico_conjuntura, artigo_ciclos_
protesto_brasil, relatorios AEP — a cotejar na redação final.

**DECISÃO PENDENTE (não incorporada — conflita com validado):** cycle_phases_v4 +
nota_consolidada_v2 trazem periodização revisada (variável traducao_institucional, código
NA≠0, fase de articulação do Fora Collor nov/1991, fase de latência no Impeachment, remoção
da radicalização em J13). Aguarda decisão do usuário (docs/tarefas.md P1) antes de substituir
data/cycle_phases.csv validado.

## 2026-07-04 — Tese de doutorado incorporada; proposta de fases de articulação

Usuário anexou a tese (Costa 2024) como fonte primária → preservada em artefatos/tese/.
Pergunta central: melhorar a fronteira Junho 2013 → Impeachment Dilma e as fases de articulação.

Achados (fundamentados na tese):
- A tese separa (Quadro 6): Ciclo Mosaico (jun/2013) → Ciclo das Eleições de 2014 →
  Ciclo Patriota (mar-abr/2015) → Ciclo do Impeachment (dez/2015-mar/2016).
- Fronteira J13→Dilma: J13 encerra em 2013; a ARTICULAÇÃO do impeachment começa após o
  2º turno de 26/10/2014, com Aécio (PSDB) contestando as urnas — mobilização eleitoral
  reativa (McAdam & Tarrow 2011; Tatagiba 2018).
- Fora Collor: fase de articulação nov/1991–mai/1992 (Mische 2008); denúncia a partir de
  01/06/1992 (CPMI PC Farias).
- Junho 2013 SEM fase de articulação: MPL tem pré-história (Revolta do Buzu 2003; MPL-Brasil
  no FSM 2005), mas as ações anteriores são "esporádicas"; a tese fixa o "divisor de águas"
  (junho é ruptura de amplitude, não desdobramento articulado). Confirma a intuição do usuário.

Proposta detalhada em docs/periodizacao-articulacao.md (não aplicada ao dataset — aguarda
confirmação; ver docs/tarefas.md P1/P2).

## 2026-07-04 — Periodização v3 aplicada (fases de articulação + latência + traducao_institucional)

Decisão do usuário (confirmando docs/periodizacao-articulacao.md):
1. Fase de ARTICULAÇÃO adotada em Diretas Já (1982-11→1983-02), Fora Collor
   (1991-11→1992-05, Mische 2008) e Impeachment Dilma (2014-10-27→2015-03-14,
   pós-eleição, Aécio contestando as urnas — McAdam & Tarrow 2011; Tatagiba 2018).
2. Fase de RADICALIZAÇÃO mantida em Junho 2013 (21/06→31/07). Verificado na tese
   (§3.3.3): a radicalização do repertório (black blocs) intensifica-se APÓS a
   violência policial contra manifestantes (13/06) e o confronto de 17/06, após o
   pico (20/06) e a retirada do MPL (21/06).
3. Fase de LATÊNCIA adotada no Impeachment (2015-08-17→2015-12-01).
4. Variável traducao_institucional (0-3) incorporada (9ª variável).

data/cycle_phases.csv reescrito: 24 fases (6 por ciclo). v2 preservada em
data/cycle_phases_v2_prearticulacao.csv. Codebook atualizado (fases articulacao/
latencia, variável traducao_institucional). Fronteira J13→Dilma redefinida: J13
encerra em 2013; articulação do impeachment inicia após 26/10/2014.

## 2026-07-04 — Relatório metodológico

Criada pasta metodologia/ com relatorio-metodologico.md: relatório acadêmico-científico
descritivo e estruturado de todas as etapas do projeto — abordagem teórico-metodológica,
desenho e periodização (v3, 24 fases), prospecção e coleta de dados (pipeline AEP/Acervo
Folha, scraping, codebook DoCA/BEP/MPEDS, bancos NEPAC e Mass Mobilization, sementes,
validação de cronologia), governança do repositório, insights produzidos, limitações e
cronologia das etapas. Documento vivo.
