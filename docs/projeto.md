# Projeto: Ciclos de Protesto no Brasil — EOP, DOS e Análise de Conjuntura

Agenda pós-defesa de doutorado de Gustavo Paccelli Costa (Tese: *Estruturas de
mobilização e oportunidades políticas: análise dos ciclos de protestos no Brasil
contemporâneo*, UFJF, 2024). Este repositório consolida e dá continuidade ao
trabalho desenvolvido nas sessões anteriores (abr–jun/2026).

## Arquitetura do projeto

### 1. Artigo teórico — o triângulo EOP–DOS–Análise de Conjuntura
Integração da Teoria do Processo Político (EOP + DOS) com a tradição brasileira
de análise de conjuntura, ancorada nos conceitos de conjunturas críticas
(della Porta 2018, 2022; Mariano, Ferreira & Neves 2023) e conjunturas fluidas
(Dobry 1986). Estudo de caso comparativo dos ciclos analisados na tese
(Fora Collor, Junho 2013, Impeachment Dilma).
Estado: seções redigidas (introdução, seção DOS, metodologia, estudo de caso
4.1–4.5, discussão conclusiva, referências ABNT) — ver `artigo/`.

**Quatro padrões de articulação identificados:**
1. Convergência EOP+DOS (Fora Collor) → mobilização massiva com resultado previsível
2. Abertura caótica EOP+DOS (Junho 2013) → alta mobilização sem resultado institucional definido
3. Construção deliberada de EOP+DOS (Impeachment) → resultado definido por atores estratégicos
4. Assimetria DOS → polarização e disputa de legitimidade

### 2. Projeto comparativo — 4 ciclos com codebook `cycle_phases`
Comparação dos quatro ciclos (Diretas Já, Fora Collor, Junho 2013, Impeachment
Dilma) com periodização em 5 fases e 8 variáveis (5 OP + 3 OD), escala 0–3.
- Codebook: `codebook/cycle_phases_codebook.yaml`
- Dados (scores validados em 2026-06-05): `data/cycle_phases.csv`

### 3. Quadro de hipóteses (14 hipóteses, 3 famílias)
- **Família H1 (político-institucional)**: abertura do sistema; vulnerabilidade
  das elites (H1.2 — com DOS como variável moderadora; desenho de teste já
  elaborado: process tracing nos casos brasileiros + comparação Coreia 2016
  (Kwak 2021), Paraguai 2012 (Hatab 2023), Belarus 2020 (Stykow 2022));
  efeito da repressão; aliados intrainstitucionais.
- **Família H2 (discursiva)**: hegemonia discursiva; fragmentação da DOS;
  ressonância cultural; construção deliberada de oportunidades discursivas;
  feeling rules (Bröer & Duyvendak 2009).
- **Família H3 (modelo integrado)**: convergência EOP+DOS; capacidade de leitura
  conjuntural como variável independente; H3.3 — conjunturas críticas exigem
  diagnóstico simultâneo de EOP aberta + DOS fluida; assimetria discursiva como
  legado; efeitos de legado sobre o ciclo subsequente.
> Pendência: o quadro completo das 14 hipóteses (com VI, VD, indicadores e
> evidência âncora) está no .docx gerado em sessão anterior — incorporar ao
> repositório quando disponível.

### 4. Pipeline PEA — `protest_events` via Acervo Folha
- `01_scraper.py` (Playwright, login Acervo Folha, busca incremental)
- `02_doca_coder.py` (API Anthropic, system prompt DoCA, JSON validado)
- `03_build_dataset.py` (CSV/XLSX multi-aba)
- `04_intercoder_reliability.py` (Cohen's Kappa)
- Config: `.env`, `queries.yaml`, `doca_codebook.yaml`
> Pendência: scripts gerados em sessão anterior (ZIP) — incorporar ao
> repositório; execução depende de credenciais do Acervo Folha.

## Frentes abertas (prioridade)
1. **(B) Refinamento da periodização** — possível fase de radicalização em
   Junho 2013 (entre expansão e pico); lacunas no ciclo Dilma
   (2015-09→2015-11; 2016-04-18→2016-05-11); decidir início do ciclo Dilma
   (2014-10-26, dia seguinte à reeleição, vs. mar/2015).
2. **(C) Estratégia de inferência causal** — process tracing por caso
   (Bengtsson & Ruonavaara 2017; Mahoney 2001) + comparação sistemática
   (most similar/most different); operacionalizar o teste de H1.2 com os
   indicadores de vulnerabilidade (aprovação Datafolha/Ibope; votações nominais
   da Câmara; declarações de aliados; posição do Judiciário/MP).
3. **(D) Construção do banco `protest_events`** — incorporar e executar a
   pipeline DoCA quando houver credenciais.

## Materiais complementares
- `experiments/` — memorandos analíticos exploratórios (sessão 2026-06-10)
  com matrizes qualitativas EOP+DOS por ciclo e fontes verificadas; convergem
  com os padrões do artigo e alimentam as justificativas dos scores.
- `literature/survey.md` — levantamento bibliográfico complementar.
