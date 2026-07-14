# Incorporação da pasta `artefatos/` — inventário e parecer

Data: 2026-07-04. A pasta `artefatos/` reúne produtos das conversas do pesquisador em um
Projeto do claude.ai. Este documento registra o parecer sobre cada artefato: **incorporado**,
**superado** (defasado em relação ao repo — ignorado quanto a conteúdo, mas preservado) ou
**fonte para a Frente C** (material de redação do artigo). Nada foi deletado — a pasta
`artefatos/` permanece íntegra como arquivo.

## Regra aplicada
Instrução do usuário: incorporar o que **incrementa** o projeto; ignorar o que está
**defasado** em relação ao que já construímos. Bancos de terceiros continuam separados
(`data/bancos-externos/`); os artefatos são material do próprio projeto.

---

## 1. `fases_ciclos/` — periodização, sementes e referências

| Artefato | Parecer | Ação |
|---|---|---|
| `protest_events_diretas_seed.xlsx` (59 eventos) | **INCORPORADO** | → `data/protest_events_seeds/protest_events_diretas_ja_seed.csv` |
| `protest_events_fora_collor_seed.xlsx` (15 eventos) | **INCORPORADO** | → `data/protest_events_seeds/protest_events_fora_collor_seed.csv` |
| `referencias_ciclos_protesto.bib` (37 entradas) | **INCORPORADO (parcial)** | 14 referências ausentes adicionadas à ABNT |
| `referencias_ciclos_protesto.md` | fonte | versão formatada do `.bib`; consultada |
| `cycle_phases_v4.xlsx` | **DECISÃO PENDENTE** (ver §4) | periodização diverge da validada |
| `cycle_phases_v2.xlsx`, `v3.xlsx` | superado | versões intermediárias do v4 |
| `cycle_phases.xlsx` (v1) | superado | equivale ao nosso `data/cycle_phases.csv` inicial |
| `nota_teorico_metodologica.docx` | superado por → | versão de trabalho da nota consolidada |
| `nota_consolidada_v2.docx` | **DECISÃO PENDENTE** (ver §4) | documenta `traducao_institucional`, NA≠0, periodização revisada |
| `fase_articulacao_fora_collor.docx` | **DECISÃO PENDENTE** (ver §4) | fase de articulação (nov/1991–mai/1992) via Mische 2008 |

## 2. `estruturas_quadro_hip/` — hipóteses e artigo

| Artefato | Parecer | Ação |
|---|---|---|
| `quadro_hipoteses_EOP_DOS_conjuntura.docx` | superado | já incorporado em `docs/quadro-hipoteses.md` (14 hipóteses) |
| `EOP_DOS_Conjuntura_Artigo_Completo_v1.docx` | **fonte Frente C** | versão completa v1 do artigo; cotejar na consolidação |
| `artigo_H12_vulnerabilidade_elites_protestos_brasil.docx` | **fonte Frente C** | desenvolve H1.2 (vulnerabilidade das elites) |
| `artigo_processo_politico_conjuntura.docx` | **fonte Frente C** | versão do artigo com foco na análise de conjuntura |
| `Estruturas-de-oportunidades-políticas-em-Ciclos-de-protesto.md` | fonte | notas de EOP |

## 3. `mapeamamento/` — pipeline e relatórios

| Artefato | Parecer | Ação |
|---|---|---|
| `pea_acervo_folha/` (pipeline completo) | superado | é o **original** do nosso `pipeline/`, já reconstruído e evoluído (BEP+MPEDS). Ver §5 |
| `pea_acervo_folha/config/doca_codebook.yaml` | **INCORPORADO (parcial)** | `valences` (pró/anti/indeterminado) adicionadas ao nosso codebook |
| `relatorio_aep_brasil_1985_2016.docx` | **fonte Frente C/E** | relatório AEP dos 4 ciclos; base para análise |
| `relatorio_ciclos_protesto_academico.docx` | **fonte Frente C/E** | cronologias, atores, repertórios, desfechos dos 4 ciclos |
| `artigo_ciclos_protesto_brasil.docx` | **fonte Frente C** | versão do artigo (1985–presente) com abstract EN |
| `Mapeamento-de-protestos-no-Brasil-desde-1985.md` | fonte | mapeamento-síntese |

---

## 4. DECISÃO PENDENTE — periodização e esquema de codificação

Os artefatos `cycle_phases_v4.xlsx` + `nota_consolidada_v2.docx` representam uma
**revisão do esquema de codificação mais recente** que a nossa `data/cycle_phases.csv`
(validada em 2026-06-10). São incrementos reais, mas **conflitam com decisões já validadas**
— por isso aguardam a escolha do usuário antes de substituir o dataset:

**Novidades dos artefatos (incrementos):**
1. **Nova variável `traducao_institucional`** (escala 0–3): captura quando o resultado é
   obtido por canal institucional distinto do demandado (ex.: Diretas Já perde a emenda
   mas elege Tancredo). 9ª variável, ausente no nosso dataset.
2. **Código `NA` distinto de `0`**: separa "não se aplica" de "ausente/zero".
3. **Fase de articulação do Fora Collor** (nov/1991–mai/1992, via Mische 2008): antecipa
   o início do ciclo — no v4 a emergência do Fora Collor começa em 1991-11-01.
4. **Eventos-âncora com fontes** (`eventos_ancora_fontes`) por fase.

**Conflitos com a periodização validada (v2 no repo):**

| Ciclo | Repo (validado 2026-06-10) | Artefato v4 |
|---|---|---|
| Junho 2013 | fase **radicalização** (6 fases) | **sem** radicalização; pico estendido (5 fases) |
| Impeachment | 5 fases | fase **latência** (ago–dez/2015) → 6 fases |
| Fora Collor | início mai/1992 | início **nov/1991** (articulação) |

→ **Ação recomendada:** adotar `cycle_phases_v4` como dataset canônico e a `traducao_institucional`,
substituindo a v2, **se** o usuário confirmar a periodização revisada. Enquanto não houver
confirmação, o `data/cycle_phases.csv` validado permanece o vigente.

---

## 5. Pipeline: original vs. reconstruído

O `artefatos/mapeamamento/pea_acervo_folha/` é o **pipeline original**. Comparação do codebook:

- **Nosso** (`pipeline/config/doca_codebook.yaml`): mais evoluído — 5 blocos BEP-CEBRAP,
  campos MPEDS, event_schema completo. **Mantido como vigente.**
- **Original**: mais simples (DoCA-Stanford), mas continha `valences` (pró/anti/indeterminado)
  e `eligibility.min_participants` que faltavam → **`valences` incorporadas**.
- Os claim_codes do original (taxonomia 10xx–19xx granular) foram **preteridos** em favor
  do nosso esquema alinhado ao BEP — mas ficam disponíveis no artefato como referência
  caso se queira granularidade temática adicional.

Isso resolve a pendência do `research-log` ("doca_codebook RECONSTRUÍDO — validar contra o
original"): a validação foi feita; nosso codebook cobre e supera o original, exceto pelas
`valences`, agora incorporadas.


## 6. Arquivos adicionais das Diretas Já (upload 2026-07-14)

| Artefato | Parecer | Ação |
|---|---|---|
| `Cronologia_Diretas_Ja.xlsx` (aba Cronologia Comícios) | **INCORPORADO** | → `data/diretas_ja/comicios_cronologia.csv` (50 comícios) |
| `Manifestacoes_e_Dados_Diretas_Ja.xlsx` (aba Roteiro por Estado) | **INCORPORADO** | → `data/diretas_ja/comicios_por_estado.csv` (490 comícios por UF) |
| `Manifestacoes_e_Dados_Diretas_Ja.xlsx` (aba Grupos e Associações) | **INCORPORADO** | → `data/diretas_ja/grupos_associacoes.csv` |
| `Manifestacoes_e_Dados_Diretas_Ja.xlsx` (aba Manifestações por Mês) | **DUPLICATA — ignorada** | sobrepõe `data/protest_events_seeds/protest_events_diretas_ja_seed.csv` (seed permanece canônico) |
