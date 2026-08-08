# Motta (2015) — Oportunidades discursivas transnacionais e frames de risco (Argentina, Brasil, México)

**Referência:** MOTTA, Renata. Transnational Discursive Opportunities and Social Movement Risk Frames Opposing GMOs. **Social Movement Studies**, 2015. `[VERIFICAR: volume, número, páginas, DOI]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Por que esta é a incorporação de maior prioridade
É a única obra do levantamento que **opera a DOS empiricamente em contexto
latino-americano — incluindo o Brasil — com análise de conteúdo de jornais nacionais.**
Nosso arcabouço de DOS se apoia hoje em Koopmans & Statham (Alemanha/Itália), Koopmans &
Olzak (Alemanha), Ferree (EUA/Alemanha) e McCammon (EUA). Falta precedente empírico
regional; Motta o fornece, e com o mesmo tipo de fonte que usamos (imprensa).

## Argumento central
Pesquisa sobre frames de movimentos sociais tem sido cumulativa; recentemente passou a
estudar os **incentivos e constrangimentos estruturais** aos produtores de demanda via o
conceito de DOS, trazendo esfera pública e mídia para o centro da análise da contenção. A
autora argumenta que existe uma **DOS transnacional** que estrutura como riscos são
enquadrados nas lutas simbólicas sobre transgênicos; descreve, por análise de conteúdo de
jornais nacionais, o uso de frames de risco nos discursos públicos dos três países; e
explica as variações nacionais recorrendo a **outros componentes da DOS**: discurso de
política pública nacional, *timing* das agendas políticas, estrutura e cultura da mídia.

Conclui pela necessidade de considerar as várias dimensões das estruturas de oportunidade
— política, discursiva e econômica — e seu grau relativo de transnacionalização.

## Conceito/método aproveitável
1. **DOS decomposta em componentes** (discurso de política pública, timing de agenda,
   estrutura da mídia, cultura da mídia). Nossas três variáveis de DOS no `cycle_phases`
   — `od_visibilidade_midia`, `od_ressonancia_discursiva`, `od_legitimidade_narrativa` —
   podem ser cotejadas com essa decomposição para checar se cobrem o mesmo terreno.
2. **Análise de conteúdo de jornais como operacionalização da DOS** — método diretamente
   transponível para o nosso pipeline AEP, que hoje codifica evento mas captura pouco de
   enquadramento (temos `slogans`, `symbols`, `valence`, mas nenhuma medida de frame da
   *cobertura*).
3. Distinção entre estrutura **dada** e estrutura **transnacionalizada** — dialoga com
   nossa H2.4 (DOS construída deliberadamente).

## Onde entra no projeto
- **H2.1** (hegemonia discursiva) e **H2.3** (ressonância cultural) — precedente empírico.
- **`artigo/secoes/02-dos-secao-teorica.md`** — permite ancorar a seção de DOS em caso
  latino-americano, não só europeu/norte-americano.
- **`codebook/cycle_phases_codebook.yaml`** — cotejo das variáveis `od_*`.
