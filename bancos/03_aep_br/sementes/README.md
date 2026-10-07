# Sementes do banco `protest_events` — ciclos pré-2011

Dados de eventos de protesto **codificados manualmente** pelo pesquisador (sessões
claude.ai), extraídos de `artefatos/fases_ciclos/` e convertidos para CSV em 2026-07-04.

Cobrem os **dois ciclos mais antigos** — Diretas Já (1983-84) e Fora Collor (1992) —
justamente os que os bancos externos não alcançam bem: o Mass Mobilization começa em
1990 (poucos eventos por ano) e o NEPAC só cobre 2011-2016. Servem de **semente** para o
banco `protest_events` a ser expandido pelo pipeline AEP/DoCA (Frente D).

## Arquivos

| Arquivo | Eventos | Cobertura |
|---|---|---|
| `protest_events_diretas_ja_seed.csv` | 59 | Diretas Já (1983-11 a 1984) |
| `protest_events_fora_collor_seed.csv` | 15 | Fora Collor (1992) |

## Estrutura (Diretas Já)

`seed_id, date, cycle, phase, city, state, local, estimativas_por_fonte, n_estimativas,
est_min, est_max, est_mediana, fonte_primaria, doca_status, notes`

Destaque metodológico: cada evento traz **múltiplas estimativas de público por fonte**
(ex.: "30.000 (Veja); 50.000 (FSP); 50-60.000 (L&O)") com `est_min`/`est_max`/`est_mediana`
derivados — abordagem transparente para a divergência sistemática entre fontes já
observada na `docs/cronologia-validada.md`. Fontes: Rodrigues (2003), Bertoncelo (2007),
Leonelli & Oliveira (2004), Veja, IstoÉ, Folha de S.Paulo, Senhor.

O Fora Collor acrescenta `tab_ref`, `event` e `sectoral_char` (caráter setorial:
trabalhista, estudantil, cívico/partidário etc.), ancorado em Mische (2008).

## Proveniência e status

- Convertidos fielmente dos `.xlsx` originais em `artefatos/fases_ciclos/` (preservados).
- `doca_status` indica o estágio de codificação DoCA de cada semente.
- São **dados do próprio projeto** (não banco de terceiros) — não confundir com
  `data/bancos-externos/`. Alimentam diretamente o `protest_events` do pipeline.
