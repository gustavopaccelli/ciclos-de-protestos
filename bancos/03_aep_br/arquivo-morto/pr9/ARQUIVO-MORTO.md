# Arquivo morto — pipeline do PR #9

**Arquivado em:** 2026-10-21 (tarefa B7). Não executar, não importar, não editar.

Estes arquivos formavam um segundo pipeline de coleta, paralelo ao oficial:

| Arquivo | Onde ficava | O que fazia |
|---|---|---|
| `coleta_acervo.py` | `src/` | busca no Acervo Folha sem login, só pelo termo "protesto", com seletores genéricos |
| `load_acervo_to_doca.py` | `src/data/` | carregava o JSON da coleta no SQLite com eventos-placeholder |
| `run_doca_pipeline.py` | `src/` | orquestrava init → scrape → load |
| `PIPELINE_DOCA.md` | raiz | documentação desse pipeline |
| `scraper_acervo.yml` | `.github/workflows/` | execução diária no GitHub Actions; falhou todos os dias desde 27/09 e foi desativada em 07/10 |
| `TUTORIAL.md` | `src/data/pipeline_docs/` | tutorial que ainda mandava rodar `pipeline/01_scraper.py`, pasta que não existe mais |

## Por que foi arquivado

O pipeline oficial (`src/data/scraper.py` → `src/preprocessing/coder.py` → `build_dataset.py` → `intercoder_reliability.py`) faz login, coleta de forma incremental, usa seletores configuráveis (`config/selectors.yaml`) e as buscas do protocolo BEP (`config/queries.yaml`). O do PR #9 não fazia nada disso. Manter os dois lado a lado arriscava alguém (ou um agente) rodar o errado.

O processo vigente está descrito em `bancos/03_aep_br/README.md`. O histórico de cada arquivo continua no git (`git log --follow`).
