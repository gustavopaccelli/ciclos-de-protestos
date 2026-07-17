# Tarefas do projeto — acompanhamento

Inventário das tarefas pendentes e concluídas, organizado por frente.
Última atualização: 2026-07-17.

> Ver `research-state.yaml` (estado central) e `research-log.md` (linha do tempo de decisões).

---

## Frente C — Consolidação do artigo para preprint · **prioridade alta**

Estudo de caso já alinhado a 4 ciclos (Diretas Já incluída em 2026-07-04, subseções 4.1–4.6).

- [ ] **C1.** Montar as seções em documento único — hoje fragmentadas em `artigo/secoes/` (02 a 05); consolidar em `.md`/`.docx` contínuo e ordenado.
- [ ] **C2.** Integrar o quadro de 14 hipóteses (`docs/quadro-hipoteses.md`) como seção ou apêndice de discussão.
- [ ] **C3.** Criar a figura/diagrama do triângulo EOP–DOS–Análise de Conjuntura.
- [ ] **C4.** Redigir abstract e palavras-chave (PT e EN).
- [ ] **C5.** Revisão final ABNT e adequação às normas do periódico-alvo.
- [ ] **C6.** Conferência de datas na redação (comícios de abr/1984 e atos de out/2013) contra `docs/cronologia-validada.md`.

## Frente D — Pipeline `protest_events` (Acervo Folha) · **em pausa** (decisão do usuário)

Guardada em 2026-07-04. Ver diagnóstico completo do estado no `research-log.md`.

- [ ] **D1.** Validar os seletores CSS do `01_scraper.py` contra o site real (gargalo crítico — Acervo é React, seletores hoje são placeholders).
- [ ] **D2.** Instalar dependências (`pip install -r pipeline/requirements.txt`) e configurar `.env` com credenciais (NUNCA commitar o `.env`).
- [ ] **D3.** Validar o `pipeline/config/doca_codebook.yaml` reconstruído contra o original.
- [ ] **D4.** Primeira execução de teste + aferição de Cohen's Kappa (≥ 0,75).

## Frente E — Análise dos bancos e sementes · **PRIORIZADA** (ativa desde 2026-07-16)

Bancos prontos para uso: NEPAC (2011–2016), Mass Mobilization (1990–2020) e as sementes `protest_events` das Diretas Já e Fora Collor (`data/protest_events_seeds/`). Produtos ficam em `data/analise-triangulacao/` (ver README da pasta para o escopo).

- [x] **E0.** Pasta de produtos criada (`data/analise-triangulacao/` com README de escopo: séries temporais por ciclo, teste de fronteiras de fase, convergência entre fontes, memorando analítico). 2026-07-16.
- [ ] **E1.** Análise exploratória de triangulação — cruzar as séries dos dois bancos com as fases dos ciclos (`data/cycle_phases.csv`), corroborando picos e tendências. **Sem agregar as fontes** (não são somáveis — ver `data/bancos-externos/mass-mobilization-clark-regan-2020/livro-codigo/crosswalk-codigos.md`).
- [ ] **E2.** Usar os microdados como evidência para as hipóteses H1–H3 (repertórios, alvos, respostas estatais em Junho 2013 e Impeachment).
- [ ] **E3.** Integrar as sementes `protest_events` (Diretas Já + Fora Collor) à análise dos ciclos pré-2011 que os bancos externos não cobrem.

## Decisão pendente — periodização e esquema de codificação (dos artefatos)

Ver `docs/artefatos-incorporacao.md` §4. Os artefatos trazem uma revisão (variável
`traducao_institucional`, código NA≠0, fase de articulação do Fora Collor, fase de latência
no Impeachment, remoção da radicalização em J13) que **conflita com a periodização validada**.

- [x] **P1.** RESOLVIDO (2026-07-04): adotada periodização v3 revisada + variável `traducao_institucional`. `data/cycle_phases.csv` reescrito (24 fases); v2 preservada em `data/cycle_phases_v2_prearticulacao.csv`.
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
- [x] Dados complementares das Diretas Já incorporados (`data/diretas_ja/`: 50 comícios, distribuição estadual dos 490, atores da coalizão — 2026-07-14).
- [x] Inventário de artefatos concluído (`docs/artefatos-incorporacao.md`, 31 itens, incl. §6 uploads das Diretas Já).
- [x] Bibliografia ABNT expandida para ~94 referências (+14 do `.bib` dos artefatos).
- [x] README principal em formato de preprint (introdução, quadro metodológico, 14 hipóteses — 2026-07-17).

## Em espera (sem ação até instrução) ⏸

- **Inferência causal** — a antiga Frente C (process tracing / teste de H1.2) foi substituída pela consolidação do artigo. Material de referência preservado em `docs/projeto.md` e `docs/quadro-hipoteses.md` caso seja retomada.

---

### Sequência recomendada

**E (E1→E2→E3) → C (itens 1–6) → D (quando retomada).** Por decisão do usuário
(2026-07-16), a Frente E foi priorizada: a triangulação dos bancos com o
`cycle_phases` produz evidência empírica que alimenta diretamente a discussão do
artigo — a consolidação (C) encadeia logo depois, já incorporando os achados.
A Frente D permanece em pausa até haver credenciais do Acervo Folha.
