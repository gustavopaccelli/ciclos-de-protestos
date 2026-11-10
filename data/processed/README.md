# Dados Processados Finais

## Propósito

Pasta contendo versões finais, harmonizadas e validadas dos dados sobre ciclos de protesto. Estes são os dados "prontos para análise" usados em artigos, visualizações e relatórios.

## Subpastas

### `harmonizado/`
Versão canônica unificada de todos os eventos de protesto após triangulação.
- Deduplicação entre bases
- Resolução de conflitos de datas/localizações
- Inclusão de metadados de confiabilidade

Ainda não gerado: a pasta está vazia. Esperado conter:
- `protestos_brasil_1985-2024_harmonizado.csv` (ou similar)
- `dicionário_variáveis_harmonizado.md`
- `log_triangulacao.json` (discrepâncias resolvidas)

### `cycle_phases/`
Dados específicos de fases de cada ciclo de protesto.

Esperado conter:
- `cycle_phases.csv`: 24 fases, 6 por ciclo (emergência, expansão, pico, declínio e desfecho; articulação em todos os ciclos exceto Junho de 2013; radicalização só em Junho de 2013; latência só no Impeachment), com datas
- `cycle_phases_v2_prearticulacao.csv`: backup da periodização v2
- Documentação de critérios de delimitação de fases

## Fluxo

```
bancos/ + data/interim/ + data/triangulacao/ → scripts/analysis/ → data/processed/
                                                                       ↓
                                                          outputs/figures/ (visualizações)
                                                          outputs/tables/ (tabelas artigo)
```

## Características de Qualidade

Cada arquivo processado deve incluir:
- Data de processamento
- Script que gerou (link em `src/analysis/`)
- Número de observações
- Período coberto
- Nível de confiabilidade de cada registro

## Exemplo de Estrutura

```
processed/
├── harmonizado/
│   ├── protestos_brasil_1985-2024_harmonizado.csv
│   ├── dicionário_variáveis_harmonizado.md
│   └── log_triangulacao.json
├── cycle_phases/
│   ├── cycle_phases.csv
│   └── cycle_phases_v2_prearticulacao.csv
└── README.md
```

Responsável: Gustavo Paccelli
Última atualização: 2026-09-21
