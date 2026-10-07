# Codebook AEP-BR: eventos de protesto no Brasil, de 1983 até hoje

**Versão:** 1.0 (2026-10-07). As questões em aberto da v0.1 foram decididas (ver §6).
**Especificação legível por máquina:** [`codebook_aep_br.yaml`](codebook_aep_br.yaml), que traz 50 variáveis com o tipo, o vocabulário e os equivalentes no MM e no NEPAC.
**Âncora metodológica:** ALONSO, A.; REZENDE, P. J.; SOUZA, R. de; SOUZA, V. B. de. Análise de Eventos de Protesto: decisões metodológicas na organização do Banco de Eventos de Protesto (BEP) 2013-2016. *Plural*, v. 31, n. 2, p. 288-323, 2024. DOI [10.11606/issn.2176-8099.pcso.2024.233335](https://doi.org/10.11606/issn.2176-8099.pcso.2024.233335).
**Documentos de apoio:** [`docs/aep-protocol-bep.md`](../../../docs/aep-protocol-bep.md) (o protocolo BEP comentado) e [`config/doca_codebook.yaml`](../../../config/doca_codebook.yaml) (os vocabulários fechados).

---

## 1. Para que serve

O AEP-BR é o terceiro banco do projeto. Os outros dois, Mass Mobilization e NEPAC, são de terceiros e deixam lacunas:

| Banco | Período | Fonte | Limitação para o projeto |
|---|---|---|---|
| Mass Mobilization | 1990–2020 | imprensa internacional (Lexis-Nexis) | Tem só 224 eventos no Brasil. Exige no mínimo 50 pessoas e só inclui protestos contra o Estado |
| NEPAC | 2011–2016 | Folha de S.Paulo | Cobre só 6 anos |
| **AEP-BR** | **1983–hoje** | **imprensa nacional e diários oficiais** | **Ainda a construir** |

O AEP-BR aplica o protocolo do BEP (Alonso et al. 2024) a toda a cronologia do projeto, inclusive aos anos em que se sobrepõe ao MM e ao NEPAC. Nesses anos a sobreposição é proposital, porque é ela que permite **triangular** as fontes: comparar tendências e conferir picos.

Os três bancos **não são somados**. As diferenças de critério estão em [`../../crosswalk/crosswalk_mm_nepac_aep.md`](../../crosswalk/crosswalk_mm_nepac_aep.md).

## 2. Unidade de análise: o evento de protesto

A unidade é o **evento**, não a notícia. Uma matéria pode relatar vários eventos, e um mesmo evento pode aparecer em várias matérias.

### 2.1 Critérios de elegibilidade

O evento entra no banco somente se satisfizer os quatro critérios do BEP:

1. É uma **ação pública e coletiva**, em espaço público ou de acesso público.
2. É **organizada por atores não estatais**.
3. Expressa **contestação** de instituições, práticas ou valores, em qualquer direção política.
4. Carrega uma **reivindicação** social ou política, explícita ou simbólica.

### 2.2 Exclusões

- ação individual
- criminalidade comum sem reivindicação
- festa ou comemoração sem contestação
- ato político rotineiro, como convenção ou comício eleitoral de candidato. Comícios **por reivindicação** (Diretas Já, Fora Collor, impeachment) entram
- evento só virtual
- evento anunciado sem evidência de que aconteceu

> **Diferença em relação ao MM:** o MM exclui *rallies* e protestos contra alvos não estatais. O AEP-BR inclui os dois. Por exemplo, uma greve contra o patronato entra no AEP-BR (alvo `empresa-privada-patronato`).

### 2.3 Unitização

| Situação | Decisão |
|---|---|
| Mesmos atores, intervalo menor que 24h | um evento |
| Ação contínua, como uma ocupação de vários dias | um evento, com `data_fim` |
| Mesmos atores, interrupção maior que 24h | eventos distintos |
| Mesmo ato em cidades nomeadas diferentes | **um registro por cidade**, todos com o mesmo `evento_coordenado_id` |
| Grupos com pautas opostas no mesmo espaço | um registro por organizador, com `contra_protesto = true` |

A regra do `evento_coordenado_id` reproduz a lógica cidade-evento do NEPAC. Com ela, a contagem pode ser feita por evento ou por cidade, como no NEPAC (1.284 eventos e 2.548 linhas).

### 2.4 Regra do público

**Não há número mínimo de participantes.** Para comparar com outros bancos, o filtro é aplicado na análise: `publico_max >= 50` para o MM e `>= 2` para o NEPAC.

Registrar a **maior** estimativa em `publico_max` e a menor em `publico_min`. Todas as estimativas vão em `publico_estimativas`, com a fonte de cada uma. Exemplo: `"1.000.000 (organizadores); 300.000 (PM); 400.000 (Datafolha)"`. As sementes de Diretas Já já seguem esse formato.

## 3. Variáveis

As variáveis estão organizadas nos cinco blocos do BEP, mais um bloco de proveniência (P) e um de deduplicação (D). Na tabela, **★** marca as variáveis obrigatórias. Os vocabulários e as definições completas estão no YAML, que tem 53 variáveis.

| Bloco | Variável | Conteúdo | MM | NEPAC |
|---|---|---|---|---|
| I | `evento_id` ★ | UUID5 | `id` | `Codigo_evento` |
| I | `data_inicio` ★ / `data_fim` | data do evento, não da matéria | `start*` / `end*` | `Data_de_Inicio…` / `Data_termino…` |
| I | `cidade` ★, `cidade_ibge`, `uf` ★, `porte_cidade` | localização | `location` | `Cidade` |
| I | `local`, `local_tipo`, `local_convencional` | lugar e trajeto | — | `Local` |
| I | `ambito`, `capilaridade` | escala territorial | — | `Ambito_do_Protesto`, `Capilaridade` |
| I | `publico_max`, `publico_min`, `publico_estimativas`, `porte_manifestacao` | tamanho | `participants(_category)` | `N_Part` |
| I | `evento_coordenado_id` | ato em várias cidades | — | `Codigo_evento` |
| II | `atores` ★ (nome, especificação, organização, formalização) | quem protesta | `protesteridentity` | `Org…` |
| II | `base_social`, `ocupacao_atividade`, `organizacoes` | perfil social | — | `Base_social…`, `Ocupação/Atividade` |
| III | `repertorio` ★, `acao_objeto`, `acao_instrumento`, `simbolos` | o que fazem (ator–ação–objeto, Franzosi) | — | `Tipo_Protesto` |
| III | `greve_com_ato_publico` | só para greves: houve ação na rua | — | — |
| III | `violencia_manifestantes` | depredação ou agressão | `protesterviolence` | `Depredacao` |
| IV | `tema_codigo` ★, `tema_texto` ★, `valencia` | reivindicação | `protesterdemand1..4` | `Objetivo_1/2` |
| IV | `alvo` ★ | a quem se dirige | (só o Estado) | `Alvo_protesto` |
| IV | `slogans`, `contra_protesto` | dimensão simbólica | — | — |
| V | `presenca_policia`, `resposta_estatal`, `conflito_policia`, `conflito_entre_grupos` | interação | `stateresponse1..7` | `Presenca_policia`, `Repressao_policial`, `Confronto…` |
| V | `detidos`, `feridos`, `mortos` | resultado | `arrests`/`beatings`/`killings` | `Detidos`/`Feridos`/`Mortos` |
| V | `atos_oficiais` | decretos de GLO, Força Nacional etc. | — | — |
| P | `fontes` ★, `n_fontes` ★, `qualidade_ocr` ★ | matérias usadas e qualidade do texto | `sources` | `Identificacao_do_veiculo` |
| P | `elegivel` ★, `codificador` ★, `modelo_versao`, `confianca` ★, `ciclo`, `fase`, `notas` | controle | `protest`, `notes` | — |
| D | `evento_canonico_id`, `materia_multi_evento` | deduplicação | — | — |

### 3.1 Convenção para contagens

Esta convenção vale para `detidos`, `feridos` e `mortos`:

- `null`: a fonte não menciona.
- `-1`: houve, mas sem número.
- Inteiro `≥ 0`: o número informado.

Com essa convenção, os valores Sim/Não/NM do NEPAC convertem sem perda: NM vira `null`, Não vira `0` e Sim vira `-1` ou o número.

### 3.2 Resposta estatal

O vocabulário `resposta_estatal` amplia a escala de repressão do DoCA para cobrir as sete respostas do MM: `nenhuma`, `acomodacao`, `dispersao`, `prisoes`, `violencia` e `letal`. A variável é uma lista, porque um mesmo evento pode ter várias respostas, como no MM.

## 4. Fontes

A lista de veículos está em [`../fontes/fontes_aep_br.csv`](../fontes/fontes_aep_br.csv). Os princípios são estes:

1. **Fonte principal: um jornal de circulação nacional com acervo contínuo.** A Folha de S.Paulo cobre 1983 até hoje e é a mesma fonte do NEPAC, o que facilita a validação em 2011–2016. O BEP encontrou 92% de concordância entre Folha e Estadão em junho de 2013.
2. **Fontes secundárias completam variáveis e captam eventos pequenos.** São elas o Estadão, O Globo, o Jornal do Brasil (via Hemeroteca Digital, até 2010), a Agência Brasil e o G1 (a partir de 2006).
3. **Diários oficiais têm papel `resposta_estatal`.** O DOU e os diários estaduais documentam decretos de GLO, convocação da Força Nacional e estados de defesa. Eles alimentam `atos_oficiais`, mas **não criam evento sozinhos**, porque o protesto precisa estar relatado na imprensa.
4. **A edição impressa tem prioridade sobre a online.** Quando o veículo tem as duas (Folha a partir de 1996, outros a partir de 2006), a impressa é a fonte principal. A online só cria evento se o fato não saiu no impresso; nos outros casos, entra com `papel_fonte = complemento`. Isso mantém a série comparável desde 1983 e com o NEPAC.
5. **A fonte de cada variável fica registrada.** Cada matéria entra em `fontes` com veículo, tipo, papel, edição e `qualidade_ocr`.

### 4.1 Palavras-chave

Usar o conjunto validado pelo BEP: *manifestação, manifestante, protesto, reivindicação, greve, paralisação, passeata, concentração, ato, baderna, vândalos, depredação, black bloc*. A elas se somam termos de época para 1983–1992: *comício, caminhada, carreata, buzinaço, caras-pintadas, diretas*. Os termos novos precisam ser testados em amostra antes de entrar na busca (ver `config/queries.yaml`).

## 5. Fluxo de construção

O pipeline ainda **não roda**. O fluxo previsto tem cinco passos:

1. **Captura.** Buscar por palavra-chave e janela temporal em cada fonte e guardar a matéria íntegra em `../coleta/`.
2. **Triagem.** Aplicar os critérios do §2.1. O resultado é `elegivel`, com o motivo em `notas`.
3. **Codificação.** Pode ser humana ou feita por LLM com revisão. O LLM recebe este codebook como instrução.
4. **Deduplicação.** Agrupar por data, cidade e ator principal, gerar o `evento_canonico_id` e fazer revisão humana dos conflitos.
5. **Confiabilidade.** Montar um gold standard estratificado por ciclo. Exige-se κ ≥ 0,75 por variável, e variáveis com mais de 30% de `null` saem da análise. Os detalhes estão no [protocolo §12](../../../docs/aep-protocol-bep.md).

**Validação cruzada obrigatória:** antes de usar o AEP-BR na análise, recodificar uma amostra de 2013 e 2015 e comparar com o NEPAC (mesma fonte, Folha) e com o MM. Discrepâncias acima do esperado indicam problema de triagem ou de unitização.

## 6. Decisões da versão 1.0 (2026-10-07)

| Questão | Decisão | Por quê |
|---|---|---|
| Número mínimo de participantes | Nenhum; filtrar na análise | Segue o BEP e não perde eventos pequenos. Com o filtro, a comparação com o MM (≥ 50) e o NEPAC (≥ 2) continua possível |
| Greves | Toda greve noticiada entra; `greve_com_ato_publico` indica ação na rua | O BEP e o NEPAC tratam a greve como repertório. A flag permite separar paralisação e protesto de rua na análise |
| Comícios | Entram os contestatórios; o comício eleitoral de candidato fica fora | Sem isso, o ciclo das Diretas Já não existe no banco. Excluir o comício eleitoral evita inflar os anos de eleição |
| OCR | `qualidade_ocr` (boa/regular/ruim/nao_se_aplica) por fonte e no registro | Separa problema do texto de dúvida de interpretação. Permite medir o efeito do OCR na confiabilidade dos anos 1980–90 |
| Impresso × online | A impressa é a principal; a online só cria evento se o fato estiver ausente no impresso | Mantém a série comparável desde 1983 e com o NEPAC, que usa a Folha impressa |
| `ciclo` | Atribuído por `src/analysis/atribui_ciclo.py` a partir das datas de `cycle_phases.csv` | Consistência total com a periodização e nenhum trabalho de codificação. O script também devolve a fase (`phase_id`) |
