# Tarefas do projeto — acompanhamento

Inventário das tarefas pendentes e concluídas, organizado por frente.
Última atualização: 2026-10-07 (Frentes B e D unificadas; bibliografia atualizada).

> Ver `research-state.yaml` (estado central) e `research-log.md` (linha do tempo de decisões).

---

## Frente B — Bancos de dados e pipeline AEP-BR · **unificada em 2026-10-07**

A antiga Frente D (pipeline `protest_events`, Acervo Folha) foi incorporada aqui. Onde
uma tarefa da D e uma da B tratavam da mesma coisa, **vale a versão mais recente**; a
antiga fica no histórico abaixo com a indicação de qual tarefa a substituiu.
Os três bancos ficam em `bancos/`, um por pasta (ver `bancos/README.md`).

### Abertas

- [ ] **B4.** Baixar o MM completo do Dataverse e do GitHub (`bancos/01_mass_mobilization/download.py`) e conferir o portal do NEPAC. Bloqueado na nuvem pela rede; fazer localmente ou liberar os domínios.
- [ ] **B6.** Piloto de 2013 na Folha, validado contra o NEPAC. Absorve as antigas D1, D2 e D4. Etapas:
  1. instalar as dependências (`pip install -r requirements.txt`) e criar o `.env` a partir de `.env.example`, com as credenciais da Folha e a `ANTHROPIC_API_KEY` (nunca versionar o `.env`);
  2. validar os seletores no site real: `python src/data/scraper.py --diagnose --headed` (ajustes em `config/selectors.yaml`);
  3. coletar uma amostra pequena (cerca de 20 matérias) e codificar com `python src/preprocessing/coder.py --batch 20`, para medir o custo por matéria antes de ampliar;
  4. aferir o kappa (κ ≥ 0,75) com `src/preprocessing/intercoder_reliability.py` contra uma codificação manual da mesma amostra.
- [ ] **B7.** Decidir o que fazer com o pipeline duplicado do PR #9 (`src/coleta_acervo.py` e `src/run_doca_pipeline.py`) em relação a `src/data/scraper.py`, que é o scraper com login e incremental. Antes de reativar o workflow do GitHub Actions, revisar o `coleta_acervo.py`: hoje ele busca só "protesto", sem login e com seletores genéricos.
- [ ] **B8.** (antiga D8) Separar triagem e codificação em duas passagens no coder AEP-BR, como prevê o protocolo §11 (Passagens 2 e 3). Apontado por PAPEA. Fazer depois do piloto, quando houver dados de custo.
- [ ] **B9.** (antiga D9) Gerar um `validation_report.json` por execução do coder, com o registro obrigatório do protocolo §12.6: modelo, hash do prompt, tamanho do gold standard, κ por variável e tipologia de erro. Parte disso já vai em `modelo_versao`.

### Concluídas

- [x] **B0.** Reorganizar MM, NEPAC e AEP-BR em `bancos/` e corrigir os `metadata.json`, que tinham contagens incorretas (2026-10-07).
- [x] **B1.** Codebook AEP-BR v0.1, com crosswalk por variável para o MM e o NEPAC (2026-10-07).
- [x] **B2.** Desativar o agendamento diário do workflow "Pipeline Acervo Folha", que falhava todos os dias (2026-10-07).
- [x] **B3.** Questões em aberto do codebook decididas; codebook v1.0 (2026-10-07). Ver §6 de `codebook_aep_br.md`.
- [x] **B5.** `coder.py`, `build_dataset.py`, `intercoder_reliability.py`, `init_doca_database.py` e `check_schema_coverage.py` migrados para o AEP-BR, todos lendo o codebook por `src/preprocessing/aep_codebook.py` (2026-10-07). **Substitui a D0 e torna a D3 desnecessária.**

### Histórico da antiga Frente D

- [x] **D0.** Correção de 11 defeitos do coder e alinhamento ao codebook BEP (2026-07-18): schema de ~16 para 41 campos, regra do MAIOR público, UUID5, normalização e evento canônico no build, `protest_events_raw.csv`, kappa com 16 variáveis, `queries.yaml` alinhado ao BEP §3.1. *Substituída pela B5*: o schema agora é gerado do codebook AEP-BR (53 variáveis); as correções de regra continuam valendo.
- [x] **D3.** ~~Validar o `config/doca_codebook.yaml` reconstruído contra o original.~~ *Obsoleta pela B5*: o codebook de referência passou a ser o `codebook_aep_br.yaml`; o `doca_codebook.yaml` só fornece vocabulários, conferidos por `check_schema_coverage.py`.
- [x] **D5.** §12 do protocolo — validação da codificação por LLM (Halterman & Keith 2024; PAPEA/Haunss et al. 2025). 2026-07-18.
- [x] **D6.** Duplicata do pipeline em `docs/artefatos/mapeamento/pea_acervo_folha/` congelada com `ARQUIVO-MORTO.md`. 2026-07-18.
- [x] **D7.** Parecer sobre fontes alternativas ao Acervo Folha (`docs/fontes-alternativas.md`). Incorporado à lista de fontes do AEP-BR (`bancos/03_aep_br/fontes/fontes_aep_br.csv`). 2026-07-18.
- [x] **D10.** Revisão do scraper (`src/data/scraper.py`): seletores em `config/selectors.yaml`, modo `--diagnose`, login confirmado antes de coletar, retry, `--dry-run` e `--limit`. 2026-07-18.
- D1, D2 e D4 → incorporadas à **B6**. D8 → **B8**. D9 → **B9**.

## Frente C — Consolidação do artigo para preprint · **prioridade alta**

Estudo de caso já alinhado a 4 ciclos (Diretas Já incluída em 2026-07-04, subseções 4.1–4.6).

- [ ] **C1.** Montar as seções em documento único — hoje fragmentadas em `artigo/secoes/` (02 a 05); consolidar em `.md`/`.docx` contínuo e ordenado.
- [ ] **C2.** Integrar o quadro de 14 hipóteses (`docs/quadro-hipoteses.md`) como seção ou apêndice de discussão.
- [ ] **C3.** Criar a figura/diagrama do triângulo EOP–DOS–Análise de Conjuntura.
- [ ] **C4.** Redigir abstract e palavras-chave (PT e EN).
- [ ] **C5.** Revisão final ABNT e adequação às normas do periódico-alvo.
- [ ] **C6.** Conferência de datas na redação (comícios de abr/1984 e atos de out/2013) contra `docs/cronologia-validada.md`.

## Frente E — Análise dos bancos e sementes · **PRIORIZADA** (ativa desde 2026-07-16)

Bancos prontos para uso: NEPAC (2011–2016), Mass Mobilization (1990–2020) e as sementes `protest_events` das Diretas Já e Fora Collor (`bancos/03_aep_br/sementes/`). Produtos ficam em `data/triangulacao/series_temporais/` (ver README da pasta para o escopo).

- [x] **E0.** Pasta de produtos criada (`data/triangulacao/series_temporais/` com README de escopo: séries temporais por ciclo, teste de fronteiras de fase, convergência entre fontes, memorando analítico). 2026-07-16.
- [x] **E1.** (2026-10-07; produtos em `data/triangulacao/e1_cruzamento_mm_nepac/`: painel HTML, relatório metodológico, CSVs) Análise exploratória de triangulação — cruzar as séries dos dois bancos com as fases dos ciclos (`data/processed/cycle_phases/cycle_phases.csv`), corroborando picos e tendências. **Sem agregar as fontes** (não são somáveis — ver `bancos/crosswalk/crosswalk_mm_nepac_aep.md`).
- [ ] **E2.** Usar os microdados como evidência para as hipóteses H1–H3 (repertórios, alvos, respostas estatais em Junho 2013 e Impeachment).
- [ ] **E3.** Integrar as sementes `protest_events` (Diretas Já + Fora Collor) à análise dos ciclos pré-2011 que os bancos externos não cobrem.

## Verificação bibliográfica

A checagem automática está zerada: em 2026-10-07, `python src/analysis/check_bib.py` dá OK e
`python src/analysis/lista_verificacao.py` mostra 0 entradas marcadas `VERIFICAR`. As 26
pendências de 2026-07 foram fechadas nos commits `bib:` de 2026-08-30 a 2026-09-01; entre
elas, três eram atribuição errada e não metadado faltando (Sallum Jr. 2015, Avritzer 2016,
Ortellado 2016).

- [x] **V1.** Metadados (volume, número, páginas, DOI, coautoria) conferidos; lista de verificação zerada em 2026-09-01.
- [ ] **V2.** Ler na íntegra as obras fichadas a partir de abstract (ver aviso em
      `literature/fichamentos/README.md`) antes de citá-las no artigo.

## Decisão pendente — periodização e esquema de codificação (dos artefatos)

Ver `docs/artefatos-incorporacao.md` §4. Os artefatos trazem uma revisão (variável
`traducao_institucional`, código NA≠0, fase de articulação do Fora Collor, fase de latência
no Impeachment, remoção da radicalização em J13) que **conflita com a periodização validada**.

- [x] **P1.** RESOLVIDO (2026-07-04): adotada periodização v3 revisada + variável `traducao_institucional`. `data/processed/cycle_phases/cycle_phases.csv` reescrito (24 fases); v2 preservada em `data/cycle_phases_v2_prearticulacao.csv`.
- [x] **P2.** RESOLVIDO (2026-07-04): aplicadas as fases de articulação (`docs/periodizacao-articulacao.md`), fundamentada na tese: articulação forte no Fora Collor (nov/1991, Mische 2008) e no Impeachment Dilma (pós-eleições out/2014, Aécio contestando — McAdam & Tarrow 2011; Tatagiba 2018); Junho 2013 SEM articulação (ruptura, não articulação — confirmado pela tese); Diretas Já a decidir. Fronteira J13→Dilma redefinida.

---

## Concluídas ✅ (registro)

- [x] **Frente A / antiga B (periodização)** — periodização v2 validada (21 fases; radicalização em J13; extensões do ciclo Dilma). Ver `docs/periodizacao-revisao.md`.
- [x] Bibliografia ABNT expandida para 86 referências (`artigo/referencias-abnt.md`).
- [x] Cronologia validada com fontes institucionais; correção do comício de Goiânia (12/abr/1984). Ver `docs/cronologia-validada.md`.
- [x] Protocolo BEP-CEBRAP (Alonso et al. 2024) incorporado. Ver `docs/aep-protocol-bep.md`.
- [x] Integração MPEDS (Hanna 2017) ao codebook e ao protocolo.
- [x] Inclusão das Diretas Já como 4º ciclo do estudo de caso do artigo.
- [x] Banco NEPAC/UNICAMP (Tatagiba & Galvão 2019) incorporado — 2.548 registros / 1.284 eventos 2011–2016.
- [x] Banco Mass Mobilization (Clark & Regan v16) incorporado — 224 protestos do Brasil 1990–2020.
- [x] Periodização v3 (24 fases) validada e aplicada: fases de articulação (Diretas Já, Fora Collor, Impeachment), latência (Impeachment), radicalização mantida (J13), variável `traducao_institucional` (2026-07-04).
- [x] Relatório metodológico acadêmico criado (`metodologia/relatorio-metodologico.md`, 2026-07-04).
- [x] Dados complementares das Diretas Já incorporados (`bancos/03_aep_br/sementes/diretas_ja/`: 50 comícios, distribuição estadual dos 490, atores da coalizão — 2026-07-14).
- [x] Inventário de artefatos concluído (`docs/artefatos-incorporacao.md`, 31 itens, incl. §6 uploads das Diretas Já).
- [x] Bibliografia ABNT expandida para ~94 referências (+14 do `.bib` dos artefatos).
- [x] README principal em formato de preprint (introdução, quadro metodológico, 14 hipóteses — 2026-07-17).
- [x] Bibliografia canônica máquina-legível: `artigo/referencias.bib` (116 entradas, biblatex),
      unificando a lista ABNT, o .bib dos artefatos e 16 obras novas do levantamento de
      2026-07-18 (AEP automatizada + DOS pós-2015). Verificador `artigo/check_bib.py`.
- [x] Fichamentos analíticos de 10 obras-chave em `literature/fichamentos/`; `survey.md`
      atualizado (estava defasado desde 2026-06-10).

## Em espera (sem ação até instrução) ⏸

- **Inferência causal** — a antiga Frente C (process tracing / teste de H1.2) foi substituída pela consolidação do artigo. Material de referência preservado em `docs/projeto.md` e `docs/quadro-hipoteses.md` caso seja retomada.

---

### Sequência recomendada

**E (E1→E2→E3) → C (itens 1–6) → B (B6 quando houver credenciais).** Por decisão do
usuário (2026-07-16), a Frente E foi priorizada: a triangulação dos bancos com o
`cycle_phases` produz evidência empírica que alimenta diretamente a discussão do
artigo — a consolidação (C) encadeia logo depois, já incorporando os achados.
Na Frente B, o que não depende de credenciais (B7, B4 localmente) pode andar em paralelo;
o piloto (B6) espera as credenciais da Folha e a chave da API.
