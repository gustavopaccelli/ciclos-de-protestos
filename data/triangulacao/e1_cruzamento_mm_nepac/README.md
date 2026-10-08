# E1 — Cruzamento das séries Mass Mobilization e NEPAC com as fases dos ciclos

Produtos da tarefa E1 (Frente E). Cruza as séries de eventos do MM (1990–2020) e do NEPAC (2011–2016) com a periodização v3 e com as variáveis observáveis de EOP e DOS de cada fase. **As fontes nunca são somadas.**

| Arquivo | O que é |
|---|---|
| [`painel_e1.html`](painel_e1.html) | **Painel interativo.** É um arquivo único que abre no navegador, sem internet. |
| [`relatorio_metodologico.md`](relatorio_metodologico.md) | **Relatório metodológico.** Fundamentação, passo a passo, resultados, limitações e referências. |
| `cruzamento_series.py` | Script que gera tudo. Rode a partir da raiz: `python data/triangulacao/e1_cruzamento_mm_nepac/cruzamento_series.py` |
| `painel_modelo.html` | Modelo do painel. Edite este arquivo, e não o `painel_e1.html`, que é gerado. |
| `dados/eventos_atribuidos.csv` | Um evento por linha, com fonte, data, ciclo e fase. |
| `dados/eventos_por_fase.csv` | Fase × fonte: dias, cobertura, eventos, taxa por 30 dias com IC 95% e as variáveis de EOP e DOS. |
| `dados/linha_de_base.csv` | Taxa dentro e fora das fases de ciclo, por fonte. |
| `dados/teste_picos.csv` | Indica se a fase "pico" tem a maior taxa do ciclo. |
| `dados/associacao_eop_dos.csv` | Spearman entre a taxa e cada variável, por fonte, com p por permutação e q de Benjamini-Hochberg. |
| `dados/associacao_intraciclo.csv` | O mesmo cálculo dentro de cada ciclo, com permutação exata. |
| `dados/serie_mensal_sobreposicao.csv` | MM e NEPAC mês a mês, de jan/2011 a ago/2016. |
| `dados/convergencia_fontes.csv` | Spearman entre as duas séries mensais e os meses de pico comuns. |
| `dados/painel_dados.json` | Os mesmos resultados, no formato que o painel lê. |

## Resultados em uma linha cada

- **Concentração:** a taxa de eventos nas fases de ciclo é 3,2 vezes a de fora no MM e 1,5 vez no NEPAC.
- **Convergência:** MM e NEPAC variam juntos mês a mês (ρ = 0,37), mesmo sem junho de 2013.
- **Pico:** a fase "pico" tem a maior frequência no MM, mas não no NEPAC. Em Junho 2013, o NEPAC registra mais atos na radicalização.
- **EOP e DOS:** só a repressão acompanha a frequência de eventos (NEPAC ρ = 0,94, q = 0,001), inclusive dentro de Junho 2013. Abertura institucional e DOS não acompanham a frequência.

Os detalhes e as cautelas estão no relatório.
