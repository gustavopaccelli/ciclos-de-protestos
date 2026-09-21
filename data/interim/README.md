# Dados Intermediários (Interim)

## Propósito

Pasta para armazenar dados em processamento - entre os dados brutos (`data/raw/`) e os dados finais processados (`data/processed/`).

## Subpastas

### `nepac/`
Versão processada dos dados NEPAC após limpeza, padronização e validação.
- Remoção de duplicatas
- Normalização de nomes de cidades e estados
- Conversão de formatos
- Validação de datas e localizações

### `mass_mobilization/`
Versão processada dos dados Mass Mobilization após limpeza e harmonização.
- Filtro para Brasil
- Padronização de variáveis
- Alinhamento com dicionário de códigos brasileiro

### `seeds/`
Versão processada das sementes históricas após validação preliminar.
- Verificação de datas e localizações
- Enriquecimento com fontes adicionais
- Marcação de registros para expansão posterior

## Fluxo

```
data/raw/ → scripts/preprocessing/ → data/interim/ → triangulação → data/processed/
```

## Variáveis Esperadas

Cada subpasta deve conter:
- CSVs com dados limpos
- Logs de transformações (quantas linhas removidas, quais campos normalizados)
- Dicionário de códigos local (se houver variações)

Responsável: Gustavo Paccelli
Última atualização: 2026-09-21
