# CLAUDE.md

Pesquisa "Ciclos de Protesto no Brasil" (EOP, DOS e análise de conjuntura). Visão geral em `README.md`; estado em `research-state.yaml`; mudanças em `research-log.md`.

## Convenções

- Caminhos: importe de `src/paths.py`, não monte caminhos relativos.
- `.gitignore` bloqueia quase tudo em `data/triangulacao/`, `data/interim/` e `data/processed/`. Depois de criar arquivos ali, confira com `git check-ignore -v`. O painel E1 (PR #12) se perdeu por isso.
- Bancos de terceiros (Mass Mobilization, NEPAC) são comparados, nunca somados.
- Codificação ordinal 0–3; `NA` (não se aplica) ≠ `0` (medido e ausente). Toda alteração de codificação vai para `docs/codebook/historico-codificacao.csv`.
- Relações encontradas por inspeção do corpus já codificado são ajuste intra-amostra, não corroboração.
- Não invente fontes, números ou citações; atribua conceitos à literatura.

## Produtos

Relatórios interativos ficam em `produtos/` (publicados no GitHub Pages pelo workflow `pages.yml`). Para criar um novo, use a skill `/novo-produto`.
