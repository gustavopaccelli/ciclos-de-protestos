# Análise de triangulação — Frente E

Pasta de produtos da **Frente E**: triangulação dos bancos externos com a
codificação `cycle_phases` do projeto.

## Objetivo

Confrontar três fontes independentes (não mescladas) para validar e refinar a
periodização e os scores dos ciclos de protesto:

1. **`data/cycle_phases.csv`** — codificação ordinal do projeto (24 fases,
   9 variáveis, escala 0–3; periodização v3 validada em 2026-07-04).
2. **NEPAC/UNICAMP** (`data/bancos-externos/`) — 1.284 eventos 2011–2016
   (Acervo Folha); cobre Junho 2013 e Impeachment Dilma.
3. **Mass Mobilization** (`data/bancos-externos/`) — 224 protestos do Brasil
   1990–2020 (imprensa internacional); cobre Fora Collor em diante.
4. Complementares: `data/protest_events_seeds/` (Diretas Já 59, Fora Collor 15)
   e `data/diretas_ja/` (cronologia e distribuição estadual dos comícios).

## Produtos previstos

| Produto | Descrição |
|---|---|
| Séries temporais por ciclo | Contagem mensal de eventos por fonte, sobreposta às fases do `cycle_phases` |
| Teste de fronteiras de fase | As datas de transição (emergência→expansão→pico→declínio) coincidem com inflexões nas séries? |
| Convergência entre fontes | Onde NEPAC e MM concordam/divergem (cobertura, repertórios, participação) |
| Memorando analítico | Síntese dos achados e implicações para os scores e para o artigo (Frente C) |

Regra do projeto: os bancos permanecem **fontes independentes** — a triangulação
compara, não soma nem mescla registros (ver `data/bancos-externos/crosswalk-codigos.md`).
