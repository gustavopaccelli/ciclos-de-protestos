# Verificação dos scripts

**Atualizado em:** 2026-10-07, depois da reorganização em `bancos/`. Esta versão substitui o relatório de 2026-09-21, que afirmava compatibilidade total quando vários scripts não encontravam as entradas.

| Script | Resultado |
|---|---|
| `src/analysis/build_series_temporais.py` | Roda e reproduz `series_temporais_eventos.csv` sem diferenças: NEPAC 1.284, MM 224, Diretas Já 59, Fora Collor 15 |
| `src/analysis/check_bib.py`, `varre_citacoes.py` | Rodam e leem `docs/artigo/referencias.bib` |
| `src/preprocessing/valida_cycle_phases.py` | 0 erros, 0 avisos |
| `src/preprocessing/pt_valida_registro.py` | Nenhum problema encontrado |
| `bancos/03_aep_br/codebook/codebook_aep_br.yaml` | YAML válido; 50 variáveis; todos os vocabulários referenciados existem |
| `src/data/scraper.py`, `src/preprocessing/coder.py`, `src/coleta_acervo.py` | Só a sintaxe foi conferida: precisam de credenciais da Folha, da chave da API e das dependências de `requirements.txt` |

Contagens conferidas por leitura direta dos CSV:

- `bancos/01_mass_mobilization/dados/protestos_brasil_1990-2020.csv`: 224 linhas
- `bancos/02_nepac/dados/protestos_2011-2016.csv`: 2.548 linhas, 1.284 valores distintos de `Codigo_evento`
- sementes: Diretas Já 59 e Fora Collor 15
