# Dados de Triangulação

## Propósito

Pasta dedicada a análises de triangulação entre diferentes bases de dados de eventos de protesto. A triangulação visa:

1. **Validação cruzada**: Comparar registros entre NEPAC, Mass Mobilization, seeds históricas e Acervo Folha
2. **Identificação de discrepâncias**: Encontrar divergências de datas, locais, tamanhos ou descrições entre fontes
3. **Harmonização**: Resolver conflitos e criar versão canônica de eventos
4. **Séries temporais**: Consolidar contagens e tendências sobre ciclos

## Subpastas

### `series_temporais/`
Outputs de análises de séries temporais e agregações por período, região ou tipo de evento.
- Exemplo: `series_temporais_eventos.csv` contendo contagens mensais/semanais de protestos por ciclo

### `discrepancias/`
Registros de eventos com conflitos entre bases (datas diferentes, locais ambíguos, tamanhos discrepantes).
- Inclui relatórios de investigação e resoluções

## Fluxo de Trabalho

```
data/raw/nepac/ + data/raw/mass_mobilization/ + data/raw/seeds_historicas/ 
        ↓
data/interim/{nepac,mass_mobilization,seeds}/ [limpeza/padronização]
        ↓
data/triangulacao/ [comparação e validação]
        ↓
data/processed/harmonizado/ [versão final canônica]
```

## Variáveis de Triangulação

- `event_id_nepac` / `event_id_mm` / `event_id_seed`: IDs nas bases originais
- `data_nepac` / `data_mm` / `data_seed`: Datas registradas
- `localização_nepac` / `localização_mm` / `localização_seed`: Locais
- `discrepância_tipo`: Tipo de conflito (data, local, tamanho, descrição)
- `resolução`: Como o conflito foi resolvido (qual fonte foi privilégio, etc)
- `confiabilidade_final`: Nível de confiança no registro harmonizado

## Responsável

Gustavo Paccelli (gustavopaccelli@gmail.com)

Última atualização: 2026-09-21
