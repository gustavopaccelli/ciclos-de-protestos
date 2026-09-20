# PDFs da bibliografia

Esta pasta guarda os textos integrais das obras citadas. **Os downloads não podem ser feitos
do ambiente remoto**: o proxy bloqueia SciELO, SAGE, Cambridge, Taylor & Francis e DiVA.
O registro abaixo mantém a lacuna visível em vez de silenciosa.

| Obra | Acesso aberto? | Onde baixar | Estado |
|---|---|---|---|
| HOLDO (2019) | sim | Repositório DiVA da Universidade de Lund (texto integral) | pendente |
| STYKOW (2022) | sim | Cambridge Core, PDF do artigo em *Nationalities Papers* | pendente |
| CHENOWETH; ULFELDER (2017) | parcial | SAGE (assinatura); versão de trabalho no PRIO | pendente |
| KWAK (2021) | a verificar | *Korea Observer* via DOI 10.29152/KOIKS.2021.52.1.107 | pendente |
| HATAB (2024) | não | SAGE (assinatura institucional) | pendente |
| VIEIRA (2015) | a verificar | capítulo em coletânea; conferir na bibliografia da tese | pendente |
| VIRGENS; TEIXEIRA (2023) | sim | *Lua Nova* n. 120, SciELO | pendente |
| VELASCO E CRUZ (2000) | sim | *Educação & Sociedade* v. 21 n. 72, SciELO | pendente |
| RICCI (2018) | sim | *Saúde em Debate*, SciELO — scielo.br/j/sdeb/a/yrw7bXmFdLWLDC9zmds8PXy | pendente |
| CARLOS; DOWBOR; ALBUQUERQUE (2017) | sim | *Civitas* v. 17 n. 2, SciELO | pendente |

## Checklist de metadados

`literature/verificacao-bibliografica.md` lista as 32 entradas do `.bib` cujos metadados
estão incompletos ou não foram conferidos em fonte primária. É gerado por
`artigo/lista_verificacao.py`; ao completar uma entrada, remova a nota `VERIFICAR` do `.bib`
e regenere — ela sai da lista sozinha.

## Convenção de nomes

`sobrenome-ano-palavra-chave.pdf`, em minúsculas e sem acento — por exemplo
`holdo-2019-cooptation.pdf`. O nome deve corresponder à chave da entrada em
`artigo/referencias.bib` de forma reconhecível.

## Materiais de replicação

CHENOWETH e ULFELDER (2017) publicaram os dados e scripts em
`github.com/ulfelder/nonviolent-uprisings-replication` (três scripts em R e dois datasets).
É a base empírica do Quadro 3 da tese de Costa (2024), que ancora a bateria de indicadores do
T-1 estrutural em `process-tracing/dados/series_estruturais.csv`. Candidato natural para a
etapa de incorporação de repositórios.
