# Livro de Código — Protestos no Brasil em tempos de crise (2011–2016)

> **Fonte original:** TATAGIBA, Luciana; GALVÃO, Andreia. *Os protestos no Brasil em tempos de crise (2011-2016). 2019 — Livro de Código.*
> Transcrição estruturada em Markdown do arquivo `.docx` original (preservado em `../fonte-original/`). O conteúdo conceitual é integralmente dos autores; a formatação foi adaptada para versionamento.

Livro de código referente ao banco de dados de protestos que integra a pesquisa **"Confronto político no Brasil, da ascensão à crise dos governos petistas (2003-2016)"**.
Coordenação: Profa. Dra. Luciana Tatagiba (NEPAC) e Profa. Dra. Andréia Galvão (CEMARX). Departamento de Ciência Política e Programa de Pós-Graduação em Ciência Política da UNICAMP.

- NEPAC: https://www.nepac.ifch.unicamp.br/
- CEMARX: https://www.ifch.unicamp.br/cemarx/site/
- Banco de dados: https://nepac.ifch.unicamp.br/banco-de-dados

---

## Apresentação da fonte e instruções de coleta

- **Fonte primária:** acervo da Folha de S.Paulo (https://acervo.folha.com.br), cadernos **"Poder", "Mercado" e "Cotidiano"**, período **01/01/2003 a 31/08/2016** (o recorte deste banco cobre 2011–2016).
- **Captação:** leitura diária dos cadernos indicados. Banco montado em plataforma Access, estruturado em duas tabelas: **Tabela Geral** (informações agregadas por evento) e **Tabela Específica** (informações por cidade).
- **Exclusões:** não foram incluídas ameaças de protesto ou expectativas de realização — apenas protestos que **efetivamente ocorreram**.
- Imagens com legenda que retratem manifestações também são registradas, desde que contenham ao menos uma informação (Quando? O quê? Quem? Por quê? Onde? Como?).

## Definição de "evento de protesto"

Evento de protesto (na esteira de **Tilly, 1978**; **Olzak, 1989**) é:

1. **Ação coletiva** (≥ 2 pessoas), iniciada por grupos da sociedade, de natureza **extrainstitucional** (evento público que rompe a rotina e instaura ou ameaça instaurar algum dano), voltada a sustentar reivindicações/queixas que, se atendidas, afetariam o interesse de outras pessoas. Excluem-se ações de formação de base, reuniões com apoiadores, atuação institucional, lobby.
2. **Coletiva e não individual** — diferencia resistência individual de ação coletiva. Inclui expressões coletivas espontâneas não convocadas por organizações (ex.: panelaço).
3. **Pública e oriunda da sociedade civil** — exclui protestos de deputados contra uma lei ou de prefeitos por repasses; admite organizadores/apoiadores da sociedade política (partidos etc.).
4. **Com reivindicação** (bem material) ou expressão de crença/queixa/opinião, pela mudança ou pela manutenção de uma situação. Queima de ônibus só é protesto se feita em nome de uma causa reivindicada por algum ator.

### Evento único vs. eventos distintos

Conta-se como **evento único** quando presentes **todas** as características:
- Mesma data de início;
- Continuidade no tempo (sem interrupção);
- Mesmo objetivo principal, ainda que com diferentes ações e/ou localidades.

Os critérios incluem **tempo e conteúdo**, mas **excluem território**: manifestações do MPL em 17/06/2013 em diferentes cidades, com o mesmo objetivo, recebem o **mesmo código de evento**. Isso permite trabalhar a informação **agregada por evento** ou **desagregada por cidade**.

---

## Variáveis

### Identificação do Veículo (chave primária)
Localiza onde a notícia foi publicada. Composição: `Ano+Mês+Dia+Fonte[3 letras]+Caderno+PP_nº` — ex.: `20160622FSPC08_1`.
- **Data** = data de publicação da notícia.
- **Fonte** = jornal (sempre FSP).
- **Caderno** = Primeiro Caderno, Poder, Mercado (ou Dinheiro), Cotidiano, Sessões Especiais.
- Quando uma notícia traz vários eventos, diferenciam-se pelos dígitos finais (`_1`, `_2`, `_3`).

### Código do evento
Identifica o evento de protesto. Composição: `Ano+Mês+Dia+Base mobilizada[4 letras]+nº[2 dígitos]`.
- **Data** = data de **início** do evento (pode diferir da data da notícia).
- Um evento já noticiado repete o mesmo código (permite acompanhar a trajetória).

**Códigos de base mobilizada (4 letras):**

| Código | Base mobilizada | Exemplos |
|---|---|---|
| `TERR` | Território | sem teto, sem terra, quilombola, indígenas, atingidos por barragem, morador, ruralistas/fazendeiros |
| `IDEN` | Identidade/cultural | imigrantes, mulheres, negro, LGBT, religioso, deficientes, familiares, estudantes |
| `OCUP` | Ocupação | trabalhadores (formais/informais, cidade/campo), aposentados, empregadores, desempregados |
| `POLI` | Política | ambientalistas, ativistas de direitos humanos, militantes de partidos, ciclistas |
| `OUTR` | Outros | presos, traficantes (especificar em observações) |
| `BSHT` | Base Social Heterogênea | quando há menção a mais de duas bases sociais |
| `NMEN` | Não Mencionada | quando a notícia não permite identificar a base |

### Grupo social (variável múltipla, 4 entradas)
Categorias sociais que protestam, derivadas da informação do jornal combinada com a organização convocante e, em certos casos, com a reivindicação. Da 1ª codificação (23 grupos) reagrupados em **15 grupos**:

- **Ambientalistas** — defesa do meio ambiente e/ou direitos dos animais.
- **Coletivos ou grupos ad hoc** — autodefinidos como coletivos (ex.: Marcha da Maconha), "Ocupas" (Ocupa Cabral, Ocupa Estelita), Anonymous, Black Blocs.
- **Direitos humanos** — defesa dos direitos dos indivíduos, interpelando o Estado quanto ao uso das forças repressivas.
- **Difuso** — quando não é possível distinguir quem está na rua (comum em 2013 após a revogação da tarifa).
- **Empresários** — representantes/câmaras empresariais, proprietários dos meios de produção (cidade e campo).
- **Estudantes** — nível médio ou superior, público ou privado.
- **Familiares e amigos de vítimas** — de delito entre particulares ou envolvendo forças repressivas do Estado.
- **Grupos antipetistas** — grupos heterogêneos (identificados como "brasileiros"/"cidadãos"). Em 2015–2016, protestos convocados por MBL, Revoltados Online, Movimento Contra a Corrupção, Vem Pra Rua etc. Em 2011–2014, protestos anticorrupção com forte semelhança performativa aos do impeachment, sem organizações identificáveis (incluídos pela hipótese sobre a construção do antipetismo).
- **Grupos identitários** — mulheres, negros, LGBT, imigrantes.
- **Militantes partidários** — grupos partidários, locais e nacionais.
- **Populares e moradores** — sem teto, sem-terra, atingidos por barragens, movimentos comunitários, frentes (Frente Povo Sem Medo, Frente Brasil Popular), associações de moradores.
- **Povos originários** — indígenas e quilombolas.
- **Religiosos** — católicos, evangélicos, religiões de matriz africana etc.
- **Trabalhadores** — sindicatos, centrais, ou grupos identificados como trabalhadores (público/privado, todos os ramos, incluindo informais e terceirizados).
- **Outros** — categoria residual.

**Subclassificação dos trabalhadores:** administração pública; comércio e serviço; educação; forças de segurança, aposentados e familiares; indústria; informais; outros; rural; saúde; transporte; usuários ou consumidores.

### Reivindicação (variável múltipla, 4 entradas)
Da 1ª codificação (39 categorias) reagrupadas em **11 categorias**:

- **Governo e sistema político** — contra políticos/governos, a favor ou contra o impeachment de Rousseff, anticorrupção, instituições (PM, PF, STF, partidos), liberdade de expressão, democracia/ditadura, regulamentação da mídia.
- **Salário e condições de trabalho** — condições de trabalho, salários, benefícios, contratos, legislação trabalhista.
- **Condições de vida nas cidades** — moradia, transporte, política urbana, serviços públicos.
- **Justiça, direitos humanos e segurança** — esclarecimento de crimes (do Estado ou de particulares), segurança pública, política de drogas.
- **Políticas sociais** — saúde e educação.
- **Política econômica e setorial** — juros, impostos, privatização de portos/aeroportos, leilões de petróleo.
- **Meio ambiente e desenvolvimento** — recursos naturais (exceto terra), proteção ambiental, direitos dos animais, hidrelétricas, transposição do São Francisco, megaeventos.
- **Gênero, diversidade sexual e raça** — machismo, violência contra a mulher, aborto, união civil homoafetiva, direitos reprodutivos, questão racial, cotas.
- **Terra** — demarcação de terras indígenas/quilombolas, reforma agrária, política de assentamento.
- **Outros** — categoria residual.
- **Sem dados**.

---

## Observações sobre informações divergentes

Quando notícias sobre o mesmo evento trazem números diferentes de participantes, reproduz-se a informação **tal como apresentada na notícia**, repetindo o mesmo código de evento e gerando nova identificação de veículo. Isso preserva a rastreabilidade e a trajetória do evento na cobertura.
