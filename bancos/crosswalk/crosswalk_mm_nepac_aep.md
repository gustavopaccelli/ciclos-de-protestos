# Crosswalk de códigos — Mass Mobilization ↔ códigos do projeto

> **Natureza deste documento:** tabela de correspondência **conceitual** entre as categorias do Mass Mobilization (MM) e os códigos já existentes no projeto (`pipeline/config/doca_codebook.yaml` e banco NEPAC/Tatagiba-Galvão). **Não é uma mesclagem de dados.** Cada banco permanece uma fonte independente, com seus próprios valores intactos. Este crosswalk serve apenas para permitir leitura comparada e futuras análises cruzadas — conforme a instrução: *"Não mescle nada, trabalhe como fontes diferentes, mas que compõem o mesmo projeto."*

As correspondências abaixo são **aproximadas** e assimétricas: MM usa 7 categorias amplas de demanda; o codebook DoCA usa ~30 `claim_codes` granulares; o NEPAC usa 11 categorias de reivindicação. Um código MM pode mapear para vários códigos do projeto e vice-versa.

---

## 1. Demandas dos manifestantes

| MM `protesterdemand` | DoCA `claim_codes` (domínios) | NEPAC reivindicação |
|---|---|---|
| `labor wage dispute` | 4100 (salário/condições), 4200 (greve/pauta sindical), 4300 (contra reformas) | Salário e condições de trabalho |
| `land farm issue` | 5100 (reforma agrária), 5200 (conflitos fundiários/indígenas/quilombolas) | Terra |
| `police brutality` | 6400 (direitos humanos/violência policial) | Justiça, direitos humanos e segurança |
| `political behavior, process` | 1100 (democratização), 1200 (impeachment), 1300 (reforma política), 1400 (contra golpe), 1500 (antipartidarismo) | Governo e sistema político |
| `price increases, tax policy` | 3100 (transporte/tarifa), 4400 (custo de vida/inflação), 3500 (gastos públicos) | Condições de vida nas cidades; Política econômica e setorial |
| `removal of politician` | 1200 (impeachment/saída de governante), 2100–2300 (anticorrupção/ética) | Governo e sistema político (impeachment/corrupção) |
| `social restrictions` | 6100–6300 (identidades/direitos civis), 8200 (pauta moral-conservadora) | Gênero, diversidade sexual e raça |

> **Nota analítica:** a categoria MM `political behavior, process` é a mais frequente no Brasil (136/224) e é deliberadamente ampla — abrange desde reforma política até transição democrática. No cruzamento com o projeto, exige desagregação via leitura de `notes`/`protesteridentity` para atribuir o `claim_code` DoCA correto.

## 2. Respostas do Estado ↔ repressão

MM registra até 7 respostas estatais; o projeto DoCA usa uma escala ordinal de repressão (`repression_levels`) mais campos-flag; o NEPAC usa flags Sim/Não/NM.

| MM `stateresponse` | DoCA `repression_levels` | NEPAC (flags) |
|---|---|---|
| `accomodation` | *(fora da escala repressiva — acomodação/negociação)* | *(sem equivalente direto; oposto de repressão)* |
| `ignore` | `none` | Repressao_policial = Não/NM |
| `crowd dispersal` | `dispersão` | Repressao_policial = Sim; Presenca_policia = Sim |
| `arrests` | `prisões` | Detidos = Sim |
| `beatings` | `violência` | Feridos = Sim; Repressao_policial = Sim |
| `shootings` | `violência` (letal/potencialmente letal) | Feridos/Mortos = Sim |
| `killings` | `violência` (letal) | Mortos = Sim |

## 3. Faixas de participantes

| MM `participants_category` | DoCA `crowd_size_scale` | DoCA `crowd_size_bep` | NEPAC |
|---|---|---|---|
| `50-99` | 1 (até 100) | pequena | (valor bruto em N_Part) |
| `100-999` | 2 (101–1.000) | pequena/média | idem |
| `1000-1999` | 3 (1.001–10.000) | média | idem |
| `2000-4999` | 3 | média | idem |
| `5000-10000` | 3 | média/grande | idem |
| `>10000` | 4–5 (10.001+) | grande/mega | idem |

## 4. Violência dos manifestantes

| MM | DoCA | NEPAC |
|---|---|---|
| `protesterviolence` (0/1) | `conflict_present` + `conflict_police` (bool) | Confronto_entre_manifestantes; Depredacao |

## 5. Diferenças metodológicas relevantes (não reconciliáveis por mapeamento)

| Dimensão | MM (Clark & Regan) | Projeto DoCA/BEP e NEPAC |
|---|---|---|
| Limiar de inclusão | ≥ 50 pessoas, **alvo o Estado** | BEP: sem piso rígido; NEPAC: ≥ 2 pessoas |
| Fonte | Lexis-Nexis (imprensa internacional em inglês) | Acervo Folha de S.Paulo (imprensa nacional) |
| Alvo | **Somente antiestatal** | Inclui alvos não estatais (patronato, outros grupos) |
| Unidade | protesto–país–ano | evento (BEP); cidade-evento (NEPAC) |
| Comícios/rallies | **Excluídos** | Podem ser incluídos conforme reivindicação |

> Essas diferenças implicam que os três bancos **não são somáveis**. O MM tende a subcontar protestos locais brasileiros (viés de fonte internacional) e a excluir alvos não estatais; o NEPAC e o pipeline DoCA capturam maior granularidade nacional. O uso conjunto deve ser **triangulação** (comparar tendências, corroborar picos), não agregação.
