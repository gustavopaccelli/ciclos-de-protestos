---
name: novo-produto
description: Cria um novo relatório interativo (research report em HTML) em produtos/, publicável no GitHub Pages e no portfólio. Use quando o pesquisador pedir um novo produto, painel, relatório visual ou página interativa a partir dos dados do projeto.
---

# Novo produto em `produtos/`

Cada produto é uma pasta `produtos/<slug>/` com três arquivos, no padrão de `produtos/mapa-fases/`:

- `modelo.html` — o template. Contém `const D = /*DADOS*/null;` onde os dados entram.
- `gera.py` — lê os dados do repositório (caminhos via `src/paths.py`), valida o que lê com `assert` e grava `index.html`.
- `index.html` — gerado. Nunca editar à mão.

## Passos

1. Pergunte qual pergunta o produto responde e qual arquivo de dados ele usa. Não invente dados: só o que está versionado no repositório.
2. Copie `produtos/mapa-fases/` como ponto de partida e adapte `gera.py` e `modelo.html`.
3. Use `../estilo.css` e seus tokens de cor (claro/escuro). Sem bibliotecas externas, salvo necessidade real; nesse caso, só cdnjs com versão fixa.
4. Seções obrigatórias do relatório: Resumo, figura interativa, Método, Limitações, Dados e como citar, data de geração.
5. Redação: atribua definições à literatura ou ao codebook; nada de inferência causal além do que `research-state.yaml` admite; `NA` distinto de `0`; fontes de terceiros (MM, NEPAC) nunca somadas.
6. Rode `python produtos/<slug>/gera.py` a partir da raiz.
7. Adicione um card em `produtos/index.html`.
8. Verifique no Chromium (`executable_path="/opt/pw-browsers/chromium"`) em 375px e 1280px, claro e escuro: sem erros no console e `scrollWidth` igual à largura da janela.
9. Confirme que nada ficou ignorado: `git check-ignore -v produtos/<slug>/*` deve sair vazio.
