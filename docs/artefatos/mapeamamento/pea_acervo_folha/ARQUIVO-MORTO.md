# ⚠️ CÓPIA CONGELADA — não usar

Esta pasta é o **pipeline original**, produzido em sessão anterior do Projeto claude.ai.
Ela foi **superada** por `pipeline/`, na raiz do repositório, que é a versão vigente.

**Congelada em:** 2026-07-18. Não editar, não executar, não importar.

## Por que existe

Preservada como registro histórico, conforme a regra do projeto de não deletar artefatos
(ver `docs/artefatos-incorporacao.md`). O problema é que ela contém um
`config/doca_codebook.yaml` com o **mesmo nome e conteúdo diferente** do vigente — risco real
de alguém (ou de um agente) editar ou carregar o arquivo errado. Daí este aviso.

## O que já foi aproveitado dela

| Item | Destino |
|---|---|
| `valences` (pró / anti / indeterminado) | incorporado em `pipeline/config/doca_codebook.yaml` (2026-07-04) |
| `eligibility.min_participants` | absorvido no critério §2 do `docs/aep-protocol-bep.md` |
| taxonomia granular de claim_codes (10xx–19xx) | **preterida** em favor do esquema alinhado ao BEP; permanece aqui como referência caso se queira granularidade temática adicional |

## O que ela tinha e a versão vigente não tem

- `03_build_dataset.py` da cópia antiga emitia um **`validation_report.json`**, recurso que a
  versão vigente não reproduziu. Registrado como pendência menor — a versão vigente cobre
  parte disso pelos avisos de normalização (valores fora do codebook, ausência acima de 30%)
  emitidos em execução, mas não os persiste em arquivo.

## Versão vigente

- Pipeline: `pipeline/`
- Codebook: `pipeline/config/doca_codebook.yaml`
- Protocolo: `docs/aep-protocol-bep.md`
