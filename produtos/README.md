# Produtos

Relatórios interativos da pesquisa, em HTML autocontido, publicados no GitHub Pages pelo workflow `.github/workflows/pages.yml` a cada push na `main` que altere esta pasta.

| Pasta | Produto | Dados |
|---|---|---|
| [`mapa-fases/`](mapa-fases/) | Mapa das 24 fases (EOP, DOS e tradução institucional, 0–3) | `data/processed/cycle_phases/cycle_phases.csv` + `docs/codebook/cycle_phases_codebook.yaml` |
| [`e1-triangulacao/`](e1-triangulacao/) | Triangulação MM × NEPAC × fases (tarefa E1) | `data/triangulacao/e1_cruzamento_mm_nepac/dados/painel_dados.json`, gerado por `src/analysis/e1_cruzamento_series.py` |

## Convenções

- Uma pasta por produto: `modelo.html` (editável) + `gera.py` (injeta os dados) → `index.html` (gerado, não editar).
- Rode `python produtos/<pasta>/gera.py` a partir da raiz depois de mudar dados ou modelo.
- Estilo comum em `estilo.css` (modo claro e escuro).
- Cada relatório traz método, limitações, fonte dos dados e como citar.
- Novo produto: skill `/novo-produto` do Claude Code (`.claude/skills/novo-produto/`).

## Publicação

Ativação única: Settings → Pages → Source: **GitHub Actions**. Endereço: `https://gustavopaccelli.github.io/ciclos-de-protestos/`. Para o portfólio, linke a página ou incorpore com `<iframe src="…/mapa-fases/">`.
