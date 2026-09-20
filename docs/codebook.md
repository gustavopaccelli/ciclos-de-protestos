# Codebook: Variáveis de Eventos de Protesto

**Projeto**: Ciclos de Protesto no Brasil (1985-2024)  
**Data de Criação**: 2026-09-20  
**Última Atualização**: 2026-09-20  
**Responsável**: Gustavo Paccelli  

---

## 1. Visão Geral

Este codebook documenta o dicionário de variáveis utilizadas para codificação de eventos de protesto no projeto "Ciclos de Protesto no Brasil". Os dados cobrem múltiplos ciclos de mobilização entre 1985 e 2024.

**Período Coberto**: 1985-2024  
**Ciclos Principais**:
- Diretas Já (1983-1985)
- Fora Collor (1992)
- Junho 2013 (2011-2014)
- Impeachment de Dilma (2015-2016)

---

## 2. Variáveis de Identificação

### event_id
- **Descrição**: Identificador único do evento de protesto
- **Tipo**: String
- **Formato**: {CICLO}_{DATA}_{CIDADE}_{NUMERO}
- **Exemplo**: `diretas_ja_19830420_sao_paulo_001`
- **Obrigatório**: Sim

### ciclo_id
- **Descrição**: Identificador do ciclo de protesto ao qual o evento pertence
- **Tipo**: Categorical
- **Valores**: `diretas_ja`, `fora_collor`, `junho_2013`, `impeachment_dilma`
- **Obrigatório**: Sim

---

## 3. Variáveis Temporais

### data_evento
- **Descrição**: Data do evento de protesto
- **Tipo**: Date
- **Formato**: YYYY-MM-DD
- **Obrigatório**: Sim

### mes
- **Descrição**: Mês do evento
- **Tipo**: Integer (1-12)
- **Derivado**: Extraído de `data_evento`

### ano
- **Descrição**: Ano do evento
- **Tipo**: Integer
- **Derivado**: Extraído de `data_evento`

### fase_ciclo
- **Descrição**: Fase do ciclo de protesto em que o evento ocorreu
- **Tipo**: Categorical
- **Valores**: `articulacao`, `auge`, `desarticulacao`
- **Referência**: `docs/artefatos/fases_ciclos/`

---

## 4. Variáveis Geográficas

### localizacao_principal
- **Descrição**: Localização principal do evento
- **Tipo**: String
- **Exemplo**: "Praça da Sé, São Paulo"
- **Obrigatório**: Sim

### estado
- **Descrição**: Unidade federativa (estado) do Brasil
- **Tipo**: Categorical (sigla de 2 letras)
- **Exemplo**: SP, RJ, MG, BA
- **Obrigatório**: Sim

### municipio
- **Descrição**: Município onde ocorreu o evento
- **Tipo**: String
- **Obrigatório**: Sim

### regiao
- **Descrição**: Região geográfica do Brasil
- **Tipo**: Categorical
- **Valores**: `norte`, `nordeste`, `centro-oeste`, `sudeste`, `sul`
- **Derivado**: Baseado no estado

---

## 5. Variáveis de Características do Evento

### tipo_evento
- **Descrição**: Tipo/formato principal do evento de protesto
- **Tipo**: Categorical
- **Valores**: 
  - `manifestacao_publica` - Manifestação/protesto público
  - `comicio` - Comício político
  - `passeata` - Passeata/marcha
  - `bloqueio` - Bloqueio de rua/rodovia
  - `ocupacao` - Ocupação de espaço
  - `acampamento` - Acampamento/encampamento
  - `assembleia` - Assembleia ou reunião política
  - `outro`
- **Obrigatório**: Sim

### tamanho_estimado
- **Descrição**: Estimativa do número de participantes
- **Tipo**: Categorical
- **Valores**: 
  - `pequeno` (< 1.000)
  - `medio` (1.000-10.000)
  - `grande` (10.000-100.000)
  - `muito_grande` (> 100.000)
  - `desconhecido`

### reivindicacoes_principais
- **Descrição**: Reivindicações/demandas principais do evento
- **Tipo**: Text
- **Exemplo**: "Restauração da democracia; Anulação de decisões judiciais"
- **Notas**: Múltiplas reivindicações separadas por ponto-e-vírgula

---

## 6. Variáveis de Atores

### atores_principais
- **Descrição**: Principais grupos/organizações envolvidas
- **Tipo**: Categorical (multivalor)
- **Exemplos**: 
  - `partidos_politicos`
  - `sindicatos`
  - `movimentos_sociais`
  - `estudantes`
  - `igrejas`
  - `sociedade_civil`
  - `ciudadania_espontanea`

### lideran ca_identificavel
- **Descrição**: Se houve liderança identificável no evento
- **Tipo**: Boolean
- **Valores**: Yes/No
- **Notas**: Líderes conhecidos facilitam análise de redes

---

## 7. Violência e Repressão

### violencia
- **Descrição**: Indicador se houve violência no evento
- **Tipo**: Boolean
- **Valores**: Yes/No
- **Referência**: Ver `violencia_tipo` para detalhes

### violencia_tipo
- **Descrição**: Tipo de violência envolvida
- **Tipo**: Categorical (multivalor)
- **Valores**:
  - `policial` - Violência policial
  - `contra_ataque` - Contra-ataques de grupos rivais
  - `vandalismo` - Depredação/vandalismo
  - `nenhuma`

### prisoes
- **Descrição**: Número de prisões registradas
- **Tipo**: Integer
- **Notas**: 0 se nenhuma prisão; -1 se desconhecido

---

## 8. Cobertura Mediática

### fonte_primaria
- **Descrição**: Fonte primária de informação sobre o evento
- **Tipo**: Categorical
- **Valores**: 
  - `jornal`
  - `revista`
  - `radio`
  - `televisao`
  - `documento_oficial`
  - `relato_testemunha`
  - `arquivo`

### fonte_secundaria
- **Descrição**: Fonte secundária de verificação
- **Tipo**: String
- **Exemplo**: "Folha de S.Paulo, 1985-04-21"

### confiabilidade_fonte
- **Descrição**: Avaliação de confiabilidade da informação
- **Tipo**: Categorical
- **Valores**: `alta`, `media`, `baixa`

---

## 9. Variáveis de Codificação

### data_codificacao
- **Descrição**: Data em que o evento foi codificado
- **Tipo**: Date
- **Formato**: YYYY-MM-DD

### codificador
- **Descrição**: Identificação do codificador
- **Tipo**: String
- **Exemplo**: "GP", "AMF", "LKS"

### confiabilidade_codificacao
- **Descrição**: Nível de confiabilidade da codificação
- **Tipo**: Categorical
- **Valores**: `alta`, `media`, `baixa`
- **Notas**: Baseada em clareza das fontes e concordância entre codificadores

---

## 10. Variáveis Derivadas/Calculadas

### dias_desde_inicio_ciclo
- **Descrição**: Dias decorridos desde o início do ciclo
- **Tipo**: Integer
- **Calculado**: A partir de `data_evento` e data de início do ciclo

### posicao_ciclo
- **Descrição**: Posição relativa do evento dentro do ciclo (0-100)
- **Tipo**: Float
- **Calculado**: A partir de `dias_desde_inicio_ciclo` / duração total do ciclo

---

## 11. Referências de Codificação

- **Esquema de Codificação**: `docs/codebook/cycle_phases_codebook.yaml`
- **Validação**: Ver `src/preprocessing/valida_cycle_phases.py`
- **Histórico de Codificação**: `docs/codebook/historico-codificacao.csv`

---

## 12. Contato e Suporte

Para dúvidas sobre as variáveis, consulte:
- **Documentação Metodológica**: `docs/methodology.md`
- **Notas de Codificação**: `docs/codebook/historico-codificacao.csv`
- **Responsável Técnico**: Gustavo Paccelli (gustavopaccelli@gmail.com)
