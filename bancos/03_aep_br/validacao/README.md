# Validação do AEP-BR

Material de validação da codificação por LLM (protocolo §12, `docs/aep-protocol-bep.md`). Tudo aqui é versionado.

| Arquivo | O que é |
|---|---|
| `amostra_manual.csv` | gold standard: amostra codificada à mão, com `evento_id` e as variáveis a aferir (listas separadas por `;`) |
| `kappa_<data>.csv` | relatório de Cohen's κ por variável, gerado por `python src/analysis/run_pipeline.py --step kappa --manual bancos/03_aep_br/validacao/amostra_manual.csv` |
| `validation_report.json` | registro obrigatório do §12.6 (modelo, hash do prompt, tamanho do gold standard, κ por variável, tipologia de erro) — a implementar na tarefa B9 |

Amostra estratificada por ciclo (≥ 10% do corpus ou 100 matérias por ciclo, o que for maior — protocolo §12.3). Limiar do projeto: κ ≥ 0,75.
