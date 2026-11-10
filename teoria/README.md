# Teoria → indicadores

Esta pasta liga a teoria do processo político e a literatura sobre ciclos de protesto ao codebook do AEP-BR. A fonte de verdade é [`matriz.yaml`](matriz.yaml): para cada conceito, a definição atribuída à literatura, as referências (chaves de `docs/artigo/referencias.bib`), o nível em que ele é observado e as variáveis do codebook que o medem.

## Duas camadas

1. **Por evento (codificado).** Atributos observáveis numa matéria: quem protesta, como, contra quem, por quê, com que resposta do Estado. São as variáveis do codebook (`bancos/03_aep_br/codebook/`).
2. **Por série (derivado).** Propriedades que a literatura atribui aos ciclos, como intensificação, difusão geográfica e setorial, inovação de repertório, coexistência de atores organizados e não organizados, radicalização e escalada repressiva. Elas só existem no conjunto dos eventos e são calculadas a partir do banco. Não se pede ao codificador, humano ou LLM, um julgamento que só a série permite.

Há ainda atributos do sistema político (abertura institucional, alinhamentos, divisão de elites) que não aparecem no evento: são **contexto externo**, hoje medido por fase em `data/processed/cycle_phases/cycle_phases.csv`.

## Status

| Status | Significado |
|---|---|
| `coberto` | medido por variáveis existentes |
| `parcial` | medido em parte; a nota diz o que falta |
| `a_criar` | candidata a variável na v1.1 do codebook, com risco de confiabilidade declarado; **a decisão é do pesquisador** |
| `derivado` | propriedade da série, calculada a partir do banco |
| `contexto_externo` | vem de outra fonte; não se observa no evento |
| `fora_do_alcance` | a imprensa não permite observar de forma confiável |

## Matriz

Tabela gerada da `matriz.yaml`. Para alterar, edite o YAML e rode `python src/preprocessing/valida_matriz.py`, que também confere as chaves do `.bib` e os nomes de variáveis (e roda no CI com `--check`).

<!-- MATRIZ:INICIO — gerado por src/preprocessing/valida_matriz.py, não editar à mão -->
| Dimensão | Conceito | Nível | Status | Variáveis ou candidata | Referências |
|---|---|---|---|---|---|
| Estrutura de oportunidades políticas (EOP) | Abertura do acesso institucional | externo | contexto_externo | — | tarrow2011power, kriesi1995new, mcadam1982political |
| Estrutura de oportunidades políticas (EOP) | Instabilidade dos alinhamentos políticos | externo | contexto_externo | — | tarrow2011power |
| Estrutura de oportunidades políticas (EOP) | Divisão entre elites | externo | contexto_externo | — | tarrow2011power, mcadam2001dynamics |
| Estrutura de oportunidades políticas (EOP) | Aliados influentes | evento | a_criar | proposta: `aliados_institucionais` (hoje: `atores`, `organizacoes`) | tarrow2011power, kriesi1995new |
| Interação com o Estado | Repressão e facilitação | evento | coberto | `presenca_policia`, `resposta_estatal`, `conflito_policia`, `detidos`, `feridos`, `mortos`, `atos_oficiais` | tilly1978mobilization, davenport2007state, tarrow2011power |
| Interação com o Estado | Escalada repressiva ao longo do ciclo | serie | derivado | `resposta_estatal`, `detidos`, `feridos`, `mortos`, `data_inicio` | tarrow2011power |
| Estruturas de mobilização | Organizações e formalização dos atores | evento | coberto | `atores`, `organizacoes`, `base_social`, `ocupacao_atividade` | mcadam1982political, tilly1978mobilization |
| Estruturas de mobilização | Coalizões e coordenação entre organizações | serie | derivado | `atores`, `organizacoes`, `evento_coordenado_id` | mcadam2001dynamics |
| Enquadramento e oportunidades discursivas (DOS) | Reivindicações e alvos | evento | coberto | `tema_codigo`, `tema_texto`, `alvo`, `ambito`, `valencia` | franzosi2004words, alonso2024analise, tilly2015contentious |
| Enquadramento e oportunidades discursivas (DOS) | Tarefas de enquadramento (diagnóstico, prognóstico, motivação) | evento | parcial | `tema_texto`, `slogans` | snow1988ideology, benford2000framing |
| Enquadramento e oportunidades discursivas (DOS) | Enquadramentos-mestre do ciclo | serie | derivado | `tema_codigo`, `slogans`, `atores` | snow1992master |
| Enquadramento e oportunidades discursivas (DOS) | Visibilidade discursiva | evento | parcial | `fontes`, `n_fontes` | koopmans2004discursive, koopmans1999ethnic |
| Enquadramento e oportunidades discursivas (DOS) | Ressonância e legitimidade discursivas | evento | a_criar | proposta: `reacoes_publicas` | koopmans2004discursive, ferree2003resonance, mccammon2007movement |
| Enquadramento e oportunidades discursivas (DOS) | Enquadramento do protesto pela imprensa | evento | a_criar | proposta: `tom_cobertura` | koopmans2004discursive, earl2004use |
| Repertório de ação | Repertório de ação | evento | coberto | `repertorio`, `acao_objeto`, `acao_instrumento`, `simbolos`, `local_tipo`, `local_convencional`, `greve_com_ato_publico` | tilly1978mobilization, tilly2006regimes, tilly2015contentious |
| Repertório de ação | Inovação e modularidade do repertório | serie | derivado | `repertorio`, `atores`, `data_inicio`, `uf` | tarrow2011power |
| Repertório de ação | Radicalização e institucionalização | serie | derivado | `repertorio`, `violencia_manifestantes`, `local_convencional`, `atores` | tarrow2011power |
| Interação com o Estado | Contramovimentos | evento | coberto | `contra_protesto`, `conflito_entre_grupos`, `valencia` | meyer1996movements |
| Dinâmica do ciclo de protesto | Intensificação do conflito | serie | derivado | `data_inicio`, `publico_max`, `publico_min`, `porte_manifestacao`, `capilaridade`, `evento_canonico_id` | tarrow2011power, tatagiba2014ciclos |
| Dinâmica do ciclo de protesto | Difusão geográfica e mudança de escala | serie | derivado | `uf`, `cidade`, `cidade_ibge`, `porte_cidade`, `ambito`, `evento_coordenado_id`, `data_inicio` | tarrow2011power, mcadam2001dynamics |
| Dinâmica do ciclo de protesto | Difusão entre setores sociais | serie | derivado | `base_social`, `ocupacao_atividade`, `atores`, `tema_codigo` | tarrow2011power |
| Dinâmica do ciclo de protesto | Atores organizados e não organizados | serie | derivado | `atores`, `organizacoes` | tarrow2011power |
| Dinâmica do ciclo de protesto | Fases do ciclo | externo | contexto_externo | `ciclo`, `fase` | costa2024estruturas, tatagiba2014ciclos |
| Dinâmica do ciclo de protesto | Emoções e dimensão cultural | evento | fora_do_alcance | — | goodwin1999caught, jasper2016protest |
| Viés da fonte (dados de imprensa) | Viés de seleção da imprensa | serie | parcial | `fontes`, `n_fontes`, `publico_max`, `porte_cidade`, `violencia_manifestantes` | earl2004use, fillieule2003appendix, hutter2014protest |
| Viés da fonte (dados de imprensa) | Viés de descrição e qualidade do texto | evento | coberto | `fontes`, `qualidade_ocr`, `confianca`, `publico_estimativas`, `codificador`, `modelo_versao` | earl2004use, franzosi2004words, alonso2024analise |
<!-- MATRIZ:FIM -->

## Regras

- Toda variável nova do codebook nasce de um conceito desta matriz, ou de uma necessidade operacional (identificação, proveniência, deduplicação) declarada como tal.
- Só entram referências que já estão no `.bib`. Definições são paráfrases atribuídas aos autores; o texto não define o fenômeno em termos absolutos.
- As candidatas `a_criar` são testadas no piloto (B6) antes de entrar no codebook: cada uma precisa atingir κ ≥ 0,75 no gold standard.
