# Event Coreference Resolution for Contentious Politics Events (arXiv:2203.10123)

**Referência:** Event Coreference Resolution for Contentious Politics Events. arXiv:2203.10123, 2022. `[VERIFICAR: autores, publicação final]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Argumento central
Propõe um conjunto de dados para **resolução de correferência de eventos**, construído a
partir de amostras aleatórias de múltiplas fontes, idiomas e países. Achado quantitativo
central: **quase metade das menções de evento em um documento coocorrem com outras
menções de evento** — o que torna inevitável obter informação errada ou parcial se a
correferência não for resolvida. A literatura anterior sobre coleta de informação de
eventos não havia quantificado a contribuição dessa etapa.

## Por que isto importa diretamente para nós
É exatamente o problema do **`canonical_event_id`** — o §10 do nosso protocolo define três
níveis de deduplicação (artigo → evento codificado → evento canônico) e delega a
canonização a "editor humano ou algoritmo futuro". O algoritmo continuava não existindo.

A implementação atual em `03_build_dataset.py` (2026-07-18) usa um critério determinístico
e auditável — mesma data + mesma localidade (cidade+UF) + mesma demanda principal — com
limites declarados: **não trata contiguidade geográfica nem sobreposição parcial de datas**.
Esta literatura indica que o problema é maior do que o critério resolve, e que o custo de
ignorá-lo é alto (informação parcial em ~metade dos casos, no corpus deles).

## Onde entra no projeto
- **`docs/aep-protocol-bep.md` §10** — deve passar a citar esta literatura ao declarar o
  limite do critério implementado.
- **`pipeline/03_build_dataset.py`** — referência para uma versão futura do agrupamento
  canônico (baseada em similaridade, não em chave exata).
- **`docs/aep-protocol-bep.md` §12.4** — "unitização" como tipo de erro próprio na
  tipologia, distinto de erro de categorização, é consequência direta deste ponto.
