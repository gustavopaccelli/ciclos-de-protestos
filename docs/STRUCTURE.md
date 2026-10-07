# Estrutura do repositório

**Atualizado em:** 2026-10-07. Esta versão substitui a de 2026-09-21, que descrevia caminhos e contagens que não correspondiam aos arquivos.

```
bancos/                     uma pasta por banco de dados (ver bancos/README.md)
  01_mass_mobilization/     MM v16, recorte Brasil 1990–2020 (224 eventos)
  02_nepac/                 NEPAC/Unicamp 2011–2016 (1.284 eventos / 2.548 linhas)
  03_aep_br/                banco próprio 1983–hoje: codebook/, fontes/, sementes/, coleta/
  crosswalk/                correspondência de categorias MM ↔ NEPAC ↔ AEP-BR
data/
  interim/                  saídas intermediárias do codificador (JSON por matéria)
  processed/cycle_phases/   dataset central de fases × ciclos (v3) e backup v2
  processed/harmonizado/    saída do build_dataset.py (vazia até a coleta)
  triangulacao/             séries temporais por fonte (Frente E) e discrepâncias
src/
  paths.py                  todos os caminhos do projeto; os scripts importam daqui
  data/                     scraper da Folha, banco SQLite, coleta de process tracing (pt_*)
  preprocessing/            codificador LLM, build_dataset, kappa, validadores
  analysis/                 séries temporais, bibliografia, predições
  coleta_acervo.py, run_doca_pipeline.py   pipeline do PR #9 (Scrapling + SQLite)
config/                     doca_codebook.yaml (vocabulários), queries.yaml, selectors.yaml
docs/
  codebook/                 codebook do cycle_phases e histórico de codificação
  process_tracing/          PROTOCOLO, codebook-evidencia.yaml, ciclos/, dados/, fontes/
  methodology/, experiments/, artigo/ (referencias.bib e ABNT), artefatos/ (material importado)
artigo/secoes/              seções redigidas do artigo
literature/                 fichamentos e levantamento bibliográfico
.github/workflows/          scraper_acervo.yml (somente disparo manual)
```

## Regras

- **Dados de terceiros ficam em `bancos/<banco>/`**, com quatro partes: `fonte-original/` (sem alteração), `dados/` (CSV UTF-8), `livro-codigo/` e `metadata.json`.
- **Bancos não se somam.** O uso conjunto é por triangulação (ver `bancos/crosswalk/`).
- **Os caminhos ficam em `src/paths.py`.** Ao mover uma pasta, atualizar só esse arquivo.
- **Arquivos derivados** (`referencias-abnt.md`, `fontes-de-dados.xlsx`, `series_temporais_eventos.csv`) são gerados por script e não devem ser editados à mão.
