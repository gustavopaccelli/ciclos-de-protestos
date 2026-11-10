# E1 — Cruzamento das séries Mass Mobilization e NEPAC com as fases dos ciclos

Produtos da tarefa E1 (Frente E). Cruza as séries de eventos do MM (1990–2020) e do NEPAC (2011–2016) com a periodização v3 e com as variáveis observáveis de EOP e DOS de cada fase. **As fontes nunca são somadas.**

> **Reconstrução (2026-10-13).** Os arquivos da primeira versão (2026-10-07) não entraram no git porque o `.gitignore` bloqueava esta pasta, e se perderam. O script foi reimplementado a partir das decisões de método do `research-log.md`; a comparação com os números originais está no painel e no log. O `.gitignore` agora versiona `dados/`.

| Arquivo | O que é |
|---|---|
| [`produtos/e1-triangulacao/`](../../../produtos/e1-triangulacao/) | **Painel interativo e relatório metodológico** (método, resultados, limitações, referências). Arquivo único, abre no navegador sem internet. |
| [`src/analysis/e1_cruzamento_series.py`](../../../src/analysis/e1_cruzamento_series.py) | Script que gera os dados. Rode a partir da raiz: `python src/analysis/e1_cruzamento_series.py`; depois `python produtos/e1-triangulacao/gera.py` |
| `dados/eventos_atribuidos.csv` | Um evento por linha, com fonte, data, ciclo e fase. |
| `dados/eventos_por_fase.csv` | Fase × fonte: dias, cobertura, eventos, taxa por 30 dias com IC 95% e as variáveis de EOP e DOS. |
| `dados/linha_de_base.csv` | Taxa dentro e fora das fases de ciclo, por fonte. |
| `dados/teste_picos.csv` | Indica se a fase "pico" tem a maior taxa do ciclo. |
| `dados/associacao_eop_dos.csv` | Spearman entre a taxa e cada variável, por fonte, com p por permutação e q de Benjamini-Hochberg. |
| `dados/associacao_intraciclo.csv` | O mesmo cálculo dentro de cada ciclo, com permutação exata. |
| `dados/serie_mensal_sobreposicao.csv` | MM e NEPAC mês a mês, de jan/2011 a ago/2016. |
| `dados/convergencia_fontes.csv` | Spearman entre as duas séries mensais e os meses de pico comuns, com e sem jun/2013. |
| `dados/painel_dados.json` | Os mesmos resultados, no formato que o painel lê. |

## Resultados em uma linha cada (reconstrução)

- **Concentração:** a taxa de eventos nas fases de ciclo é 3,3 vezes a de fora no MM e 1,55 vez no NEPAC.
- **Convergência:** MM e NEPAC variam juntos mês a mês (ρ = 0,37, p ≈ 0,002); sem junho de 2013, ρ = 0,33 (p ≈ 0,007).
- **Pico:** a fase "pico" tem a maior frequência em 2 de 3 ciclos no MM e em nenhum no NEPAC. Em Junho 2013, o NEPAC registra mais atos na radicalização.
- **EOP e DOS:** após a correção de Benjamini-Hochberg, só a repressão acompanha a frequência (NEPAC ρ = 0,94, q < 0,001; dentro de Junho 2013, ρ = 0,93, p exato ≈ 0,03). Abertura institucional e DOS não acompanham a frequência.

Os detalhes e as cautelas estão no painel.
