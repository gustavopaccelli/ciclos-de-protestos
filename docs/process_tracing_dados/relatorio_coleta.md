# Relatório de coleta — 2026-08-22

Hosts alcançáveis: 0 de 6.

## Conectividade

| Host | Estado | Detalhe |
|---|---|---|
| `dadosabertos.camara.leg.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |
| `legis.senado.leg.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |
| `api.bcb.gov.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |
| `servicodados.ibge.gov.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |
| `dadosabertos.tse.jus.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |
| `imagem.camara.gov.br` | BLOQUEADO | Tunnel connection failed: 403 Forbidden |

## Execuções

Nenhuma execução: rede indisponível.
## Pendências que nenhum script resolve

Os Diários da Câmara e do Congresso digitalizados são imagem, sem API e sem
indexação de texto. As páginas exatas estão em `fontes/fontes-de-dados.csv`:

- Diário da Câmara, 30/09/1992, p. 22067 — placar do impeachment de Collor
- Diário do Congresso, 30/12/1992, p. 4811 — abertura do julgamento no Senado
- Diário do Senado, 31/08/2016 — ata do julgamento de Dilma

Abra-as manualmente e atualize `status_verificacao` e `fonte_nivel` no registro.

## Depois da coleta

```bash
python process-tracing/scripts/valida_registro.py --estrito
python process-tracing/scripts/gera_planilha_fontes.py
```