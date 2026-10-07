# Tarefas do projeto — acompanhamento

Inventário das tarefas pendentes e concluídas, organizado por frente.
Última atualização: 2026-10-07 (reorganização em `bancos/` e codebook AEP-BR).

> Ver `research-state.yaml` (estado central) e `research-log.md` (linha do tempo de decisões).

---

## Frente B — Bancos de dados e codebook AEP-BR · **nova (2026-10-07)**

Os três bancos agora ficam em `bancos/`, um por pasta (ver `bancos/README.md`).

- [x] **B0.** Reorganizar MM, NEPAC e AEP-BR em `bancos/` e corrigir os `metadata.json`, que tinham contagens incorretas.
- [x] **B1.** Codebook AEP-BR v0.1, com crosswalk por variável para o MM e o NEPAC (`bancos/03_aep_br/codebook/`).
- [x] **B2.** Desativar o agendamento diário do workflow "Pipeline Acervo Folha", que falhava todos os dias.
- [x] **B3.** Questões em aberto do codebook decididas; codebook v1.0 (2026-10-07). Ver §6 de `codebook_aep_br.md`.
- [ ] **B4.** Baixar o MM completo do Dataverse e do GitHub (`bancos/01_mass_mobilization/download.py`) e conferir o portal do NEPAC. Bloqueado na nuvem pela rede; fazer localmente ou liberar os domínios.
- [ ] **B5.** Adaptar `coder.py` e `init_doca_database.py` ao `codebook_aep_br.yaml`.
- [ ] **B6.** Fazer um piloto em 2013 na Folha e validar contra o NEPAC. Antes de reativar o workflow, revisar `src/coleta_acervo.py`: hoje ele busca só "protesto", sem login e com seletores genéricos.
- [ ] **B7.** Decidir o que fazer com o pipeline duplicado do PR #9 (`src/coleta_acervo.py` e `src/run_doca_pipeline.py`) em relação a `src/data/scraper.py`, que é o scraper com login e incremental.

## Frente C — Consolidação do artigo para preprint · **prioridade alta**

Estudo de caso já alinhado a 4 ciclos (Diretas Já incluída em 2026-07-04, subseções 4.1–4.6).

- [ ] **C1.** Montar as seções em documento único — hoje fragmentadas em `artigo/secoes/` (02 a 05); consolidar em `.md`/`.docx` contínuo e ordenado.
- [ ] **C2.** Integrar o quadro de 14 hipóteses (`docs/quadro-hipoteses.md`) como seção ou apêndice de discussão.
- [ ] **C3.** Criar a figura/diagrama do triângulo EOP–DOS–Análise de Conjuntura.
- [ ] **C4.** Redigir abstract e palavras-chave (PT e EN).
- [ ] **C5.** Revisão final ABNT e adequação às normas do periódico-alvo.
- [ ] **C6.** Conferência de datas na redação (comícios de abr/1984 e atos de out/2013) contra `docs/cronologia-validada.md`.

## Frente D — Pipeline `protest_events` (Acervo Folha) · **em pausa quanto à execução**

Guardada em 2026-07-04 quanto à COLETA. Em 2026-07-18 o pipeline foi revisado e corrigido
offline (não exige credenciais): ver `research-log.md`.

- [x] **D0.** Correção de 11 defeitos de codificação e alinhamento ao codebook BEP (2026-07-18):
      schema do coder de ~16 para 41 campos; regra de público corrigida (o prompt mandava
      registrar o MENOR valor, contra o MAIOR do protocolo — enviesava toda variável derivada
      de tamanho); UUID5 sobre (url, data, cidade); normalização e `canonical_event_id` no
      build; `protest_events_raw.csv`; kappa com bool/str normalizado e 16 variáveis;
      `queries.yaml` alinhado às palavras-chave BEP §3.1 e às janelas da periodização v3;
      limiar de kappa unificado em 0,75. Novo teste `src/data/check_schema_coverage.py`.
- [x] **D5.** §12 do protocolo — validação da codificação por LLM (Halterman & Keith 2024;
      PAPEA/Haunss et al. 2025): 5 estágios, gold standard estratificado por ciclo, tipologia
      de erro, critério de escalada, registro obrigatório. 2026-07-18.
- [x] **D6.** Duplicata do pipeline em `artefatos/mapeamento/pea_acervo_folha/` congelada
      com `ARQUIVO-MORTO.md`. 2026-07-18.
- [x] **D7.** Parecer sobre fontes alternativas ao Acervo Folha (`docs/fontes-alternativas.md`):
      recomenda investigar a Hemeroteca Digital para Diretas Já e Fora Collor — lacuna que os
      bancos externos não cobrem; não adotar GDELT como fonte primária. 2026-07-18.
- [ ] **D8.** Separar triagem e codificação em duas passagens no coder (protocolo §11 prevê
      Passagens 2 e 3 distintas; o código faz uma só). Apontado por PAPEA.
- [ ] **D9.** Reintroduzir o `validation_report.json` que a cópia antiga emitia e a vigente não.
- [x] **D10.** Revisão do coletor `01_scraper.py` (2026-07-18): seletores movidos para
      `config/selectors.yaml` (editável sem Python, com lista de candidatos por grupo);
      modo `--diagnose` que grava HTML/screenshot/relatório de casamento de seletores;
      URL de busca codificada (acentos e espaços quebravam a requisição); hrefs relativos
      resolvidos; login confirmado antes de coletar; guarda contra paginação infinita;
      retry com backoff; vazamento de abas corrigido; `--dry-run` e `--limit`;
      progresso salvo por página. Testado contra fixture local.
- [ ] **D1.** Validar os seletores CSS contra o site real — **agora com ferramenta**:
      `python 01_scraper.py --diagnose --headed` produz o relatório; ajustes vão em
      `config/selectors.yaml`. Continua exigindo credenciais.
- [ ] **D2.** Instalar dependências (`pip install -r requirements.txt`) e configurar `.env` com credenciais (NUNCA commitar o `.env`).
- [ ] **D3.** Validar o `config/doca_codebook.yaml` reconstruído contra o original.
- [ ] **D4.** Primeira execução de teste + aferição de Cohen's Kappa (≥ 0,75).

## Frente E — Análise dos bancos e sementes · **PRIORIZADA** (ativa desde 2026-07-16)

Bancos prontos para uso: NEPAC (2011–2016), Mass Mobilization (1990–2020) e as sementes `protest_events` das Diretas Já e Fora Collor (`bancos/03_aep_br/sementes/`). Produtos ficam em `data/triangulacao/series_temporais/` (ver README da pasta para o escopo).

- [x] **E0.** Pasta de produtos criada (`data/triangulacao/series_temporais/` com README de escopo: séries temporais por ciclo, teste de fronteiras de fase, convergência entre fontes, memorando analítico). 2026-07-16.
- [ ] **E1.** Análise exploratória de triangulação — cruzar as séries dos dois bancos com as fases dos ciclos (`data/processed/cycle_phases/cycle_phases.csv`), corroborando picos e tendências. **Sem agregar as fontes** (não são somáveis — ver `bancos/crosswalk/crosswalk_mm_nepac_aep.md`).
- [ ] **E2.** Usar os microdados como evidência para as hipóteses H1–H3 (repertórios, alvos, respostas estatais em Junho 2013 e Impeachment).
- [ ] **E3.** Integrar as sementes `protest_events` (Diretas Já + Fora Collor) à análise dos ciclos pré-2011 que os bancos externos não cobrem.

## Verificação bibliográfica — **concluída em 2026-09-01** (em 2026-10-07, `check_bib.py` OK e `lista_verificacao.py` mostra 0 pendentes)

26 entradas do `.bib` estão marcadas `VERIFICAR` (rodar `python src/analysis/check_bib.py` para a
lista). Em 2026-08-30 fecharam-se as oito obras brasileiras: quatro saíram da lista (Ricci,
Scartezini, Ortellado, Becker) e três eram **atribuição errada, não metadado faltando** --
Sallum Jr. 2015 (o título correto é *O impeachment de Fernando Collor*, Editora 34, o que
resolve a divergência com `survey.md`), Avritzer 2016 (é o livro *Impasses da democracia no
Brasil*, não um capítulo) e Ortellado 2016 (Márcio Moretto não é coautor). Seguem abertas
Limongi 2023, a paginação de Avritzer e a página final de Ortellado.

- [ ] **V1.** Confirmar volume/número/páginas/DOI/coautoria via Scite ou Elicit. Os conectores
      caíram durante a sessão de 2026-07-18 antes da checagem. **Registrar como não-verificada
      qualquer entrada que não se confirme — não preencher por inferência.**
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

- [x] **Frente A/B** — periodização v2 validada (21 fases; radicalização em J13; extensões do ciclo Dilma). Ver `docs/periodizacao-revisao.md`.
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

**E (E1→E2→E3) → C (itens 1–6) → D (quando retomada).** Por decisão do usuário
(2026-07-16), a Frente E foi priorizada: a triangulação dos bancos com o
`cycle_phases` produz evidência empírica que alimenta diretamente a discussão do
artigo — a consolidação (C) encadeia logo depois, já incorporando os achados.
A Frente D permanece em pausa até haver credenciais do Acervo Folha.
