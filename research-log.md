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
