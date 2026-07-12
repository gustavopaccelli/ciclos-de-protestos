# Tarefas do projeto — acompanhamento

Inventário das tarefas pendentes e concluídas, organizado por frente.
Última atualização: 2026-07-04.

> Ver `research-state.yaml` (estado central) e `research-log.md` (linha do tempo de decisões).

---

## Frente C — Consolidação do artigo para preprint · **prioridade alta** (ativa)

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

## Frente E — Análise dos bancos e sementes · **nova, não iniciada**

Bancos prontos para uso: NEPAC (2011–2016), Mass Mobilization (1990–2020) e as sementes `protest_events` das Diretas Já e Fora Collor (`data/protest_events_seeds/`).

- [ ] **E1.** Análise exploratória de triangulação — cruzar as séries dos dois bancos com as fases dos ciclos (`data/cycle_phases.csv`), corroborando picos e tendências. **Sem agregar as fontes** (não são somáveis — ver `data/bancos-externos/mass-mobilization-clark-regan-2020/livro-codigo/crosswalk-codigos.md`).
- [ ] **E2.** Usar os microdados como evidência para as hipóteses H1–H3 (repertórios, alvos, respostas estatais em Junho 2013 e Impeachment).
- [ ] **E3.** Integrar as sementes `protest_events` (Diretas Já + Fora Collor) à análise dos ciclos pré-2011 que os bancos externos não cobrem.

## Decisão pendente — periodização e esquema de codificação (dos artefatos)

Ver `docs/artefatos-incorporacao.md` §4. Os artefatos trazem uma revisão (variável
`traducao_institucional`, código NA≠0, fase de articulação do Fora Collor, fase de latência
no Impeachment, remoção da radicalização em J13) que **conflita com a periodização validada**.

- [ ] **P1.** Usuário decidir entre manter a periodização v2 validada (repo) ou adotar o `cycle_phases_v4` revisado dos artefatos + variável `traducao_institucional`.
- [ ] **P2.** Confirmar a proposta de **fases de articulação** (`docs/periodizacao-articulacao.md`), fundamentada na tese: articulação forte no Fora Collor (nov/1991, Mische 2008) e no Impeachment Dilma (pós-eleições out/2014, Aécio contestando — McAdam & Tarrow 2011; Tatagiba 2018); Junho 2013 SEM articulação (ruptura, não articulação — confirmado pela tese); Diretas Já a decidir. Fronteira J13→Dilma redefinida.

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

## Em espera (sem ação até instrução) ⏸

- **Inferência causal** — a antiga Frente C (process tracing / teste de H1.2) foi substituída pela consolidação do artigo. Material de referência preservado em `docs/projeto.md` e `docs/quadro-hipoteses.md` caso seja retomada.

---

### Sequência recomendada

**C (itens 1–6) → E (11–12) → D (quando retomada).** A Frente C está mais madura e próxima de um entregável (o preprint); a análise dos bancos (E) pode alimentar a discussão do artigo, então encadeia bem logo depois. A Frente D permanece em pausa.
