# Bancos de dados de eventos de protesto

Cada banco tem sua própria pasta, com os arquivos originais, os dados, o livro de código, um README e um `metadata.json`. **Os bancos são independentes e não se somam**, porque têm critérios diferentes de inclusão, fonte e unidade. Usamos os três em conjunto para **triangular**: comparar tendências e conferir picos. O mapeamento entre eles está em [`crosswalk/`](crosswalk/crosswalk_mm_nepac_aep.md).

| Pasta | Banco | Período | Registros | Fonte dos eventos | Situação |
|---|---|---|---|---|---|
| [`01_mass_mobilization/`](01_mass_mobilization/) | Mass Mobilization (Clark & Regan, v16), recorte Brasil | 1990–2020 | 224 eventos | imprensa internacional | completo; os arquivos globais não foram baixados |
| [`02_nepac/`](02_nepac/) | NEPAC/Unicamp (Tatagiba & Galvão 2019) | 2011–2016 | 1.284 eventos em 2.548 linhas cidade-evento | Folha de S.Paulo | completo |
| [`03_aep_br/`](03_aep_br/) | **AEP-BR**, banco próprio (protocolo BEP, Alonso et al. 2024) | 1983–hoje | 74 eventos-semente (59 de Diretas Já e 15 de Fora Collor) | imprensa nacional e diários oficiais | codebook v0.1; coleta não iniciada |

## Cronologia combinada

```
          1983  1990         2000         2010  2011    2016    2020        hoje
MM                |=========================================================|
NEPAC                                           |=======|
AEP-BR    |===============================================================================>
ciclos    [C1 Diretas]  [C2 Collor 1992]                [C3 2013] [C4 2015-16]
```

- **1983–1989:** só o AEP-BR cobre o período (sementes de Diretas Já).
- **1990–2010:** o MM cobre o período com poucos eventos por ano. O AEP-BR será a série principal.
- **2011–2016:** os três bancos se sobrepõem. É a janela de validação do AEP-BR contra o NEPAC, que usa a mesma fonte (a Folha).
- **2017 em diante:** só o MM, até 2020, e o AEP-BR.

A série mensal por fonte é gerada por `src/analysis/build_series_temporais.py`. A saída fica em `data/triangulacao/series_temporais/series_temporais_eventos.csv`.

## Downloads pendentes

A rede do ambiente de nuvem bloqueia `dataverse.harvard.edu`, `nepac.ifch.unicamp.br` e `github.com`. Por isso esta organização usa só o material que já estava no repositório. Para completar:

- **MM:** rodar `python bancos/01_mass_mobilization/download.py`, localmente ou depois de liberar o domínio. O script baixa o dataset global e refaz o recorte Brasil. O repositório [github.com/MassMobilization](https://github.com/MassMobilization) também precisa ser conferido.
- **NEPAC:** verificar se o portal publicou outros arquivos além da planilha 2011–2016 e do livro de código.
