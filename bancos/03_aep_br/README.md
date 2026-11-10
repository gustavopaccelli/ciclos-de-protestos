# AEP-BR: banco próprio de eventos de protesto (1983–hoje)

Este é o banco de eventos de protesto construído pelo projeto a partir da imprensa nacional e de diários oficiais. Ele segue o protocolo do BEP (Alonso et al. 2024, *Plural* 31(2)); as decisões de método estão em `docs/aep-protocol-bep.md`.

## Estrutura: uma pasta por etapa

| Etapa | Pasta | Script | Git |
|---|---|---|---|
| Especificação | [`codebook/`](codebook/) | `codebook_aep_br.yaml` (v1.0) lido por `src/preprocessing/aep_codebook.py` | versionado |
| Fontes | [`fontes/`](fontes/) | `fontes_aep_br.csv`: veículos, períodos, acesso, prioridade | versionado |
| Gold standard histórico | [`sementes/`](sementes/) | 59 eventos de Diretas Já e 15 de Fora Collor, codificados à mão | versionado |
| 1. Coleta | `coleta/folha_acervo/` | `src/data/scraper.py` — uma matéria por JSON | **fora do git** (direitos autorais e tamanho) |
| 2. Codificação | [`codificacao/`](codificacao/) | `src/preprocessing/coder.py` — uma extração do LLM por matéria | versionado |
| 3. Banco | [`banco/`](banco/) | `src/preprocessing/build_dataset.py` — `protest_events.csv` (evento canônico) e `protest_events_raw.csv` (uma linha por extração) | versionado (`.xlsx` fora do git) |
| 4. Validação | [`validacao/`](validacao/) | `src/preprocessing/intercoder_reliability.py` — gold standard e κ | versionado |

Os caminhos ficam em `src/paths.py` (`FOLHA_RAW`, `AEP_CODIFICACAO`, `AEP_BANCO`, `AEP_VALIDACAO`). O pipeline antigo do PR #9 está em [`arquivo-morto/pr9/`](arquivo-morto/pr9/) e não deve ser usado.

## Como rodar

Tudo a partir da raiz do repositório. O orquestrador é `src/analysis/run_pipeline.py`.

**0. Preparar (uma vez).** `pip install -r requirements.txt`, `python -m playwright install chromium` e criar o `.env` a partir de `.env.example` (credenciais da Folha e `ANTHROPIC_API_KEY`; nunca versionar o `.env`). Conferir que coder e codebook estão alinhados:

```bash
python src/data/check_schema_coverage.py
```

**1. Validar os seletores antes de coletar.** O Acervo é uma aplicação React e muda de layout; sem seletores válidos a coleta retorna zero.

```bash
python src/data/scraper.py --diagnose --headed
```

O relatório em `coleta/folha_acervo/diagnose/` diz quantos elementos cada seletor encontrou. Seletor com 0 está errado: corrija em `config/selectors.yaml` (lista de candidatos, tentados em ordem) e repita.

**2. Coletar.** Retomável: o estado fica em `coleta/folha_acervo/scrape_state.json`. As buscas vêm de `config/queries.yaml`.

```bash
python src/data/scraper.py --dry-run     # lista o que coletaria
python src/data/scraper.py --limit 20    # teste pequeno
python src/analysis/run_pipeline.py --step scrape
```

**3. Codificar.** Em lotes, para controlar custo; matérias já codificadas são puladas. Modelo e esforço em `DOCA_MODEL` e `DOCA_EFFORT` no `.env`.

```bash
python src/analysis/run_pipeline.py --step code --batch 20
```

**4. Construir o banco.** Normaliza contra o codebook, deduplica por evento canônico e avisa sobre valores fora do codebook e variáveis com mais de 30% de ausência.

```bash
python src/analysis/run_pipeline.py --step build
```

**5. Validar.** Codifique à mão uma amostra estratificada por ciclo em `validacao/amostra_manual.csv` (ver [`validacao/README.md`](validacao/README.md)) e rode:

```bash
python src/analysis/run_pipeline.py --step kappa --manual bancos/03_aep_br/validacao/amostra_manual.csv
```

O relatório sai em `validacao/kappa_<data>.csv`. Limiar do projeto: κ ≥ 0,75.

## Estado atual

- Codebook v1.0 (decisões no §6 de `codebook/codebook_aep_br.md`).
- A coleta não começou: depende das credenciais de assinante da Folha.
- Próximos passos, em ordem: B9 (`validation_report.json`), B6 (piloto de 2013 validado contra o NEPAC, que usa a mesma fonte), B8 (triagem e codificação em passagens separadas). Depois, expandir para 1983–1992, onde as sementes servem de gold standard, e para 2017 em diante. Ver `docs/tarefas.md`.
- `src/data/init_doca_database.py` gera uma versão SQLite do banco (`protest_events.db`, fora do git). É opcional: o pipeline acima não depende dela.
