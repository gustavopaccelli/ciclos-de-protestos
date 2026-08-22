# Dossiê C2 — Fora Collor (1992)

**Status** estrutura criada, varredura não iniciada · **Última atualização** 2026-08-22

---

## Estatuto na tese

Estudo de caso empírico de Costa (2024). As formulações do Quadro 8 para este ciclo já
constam de `dados/quadro8_ampliado.csv` na coluna `formulacao_tese_2024` e aguardam
ancoragem em fonte oficial peça a peça — é isso que este dossiê produz.

## Fases

Ver `data/cycle_phases.csv`, prefixo `FC-`. Ciclo de 1991-11-01 a 1992-12-31.

## Janelas

- **janela_fixa** — 24 meses antes da 1ª fase; 24 meses após o desfecho.
- **janela_ancorada** — a definir a partir do desfecho do ciclo anterior (ver PROTOCOLO §3.1).

## T-1e — antecedente estrutural

A preencher por `scripts/extrai_series_estruturais.py`. Lembrete do PROTOCOLO §6.3: usar
NEPAC e Mass Mobilization para o indicador de aprendizado organizacional, **nunca** o
`protest_events` do próprio projeto — isso seria circular.

## T-1c — antecedente conjuntural

Codificar pelas quatro categorias de Souza (1986): acontecimentos, cenários, relações de
forças, articulação estrutura/conjuntura.

## T0 — o ciclo

Referenciar `docs/cronologia-validada.md` e os bancos de eventos. Acrescentar aqui o
rastro institucional paralelo: tramitação, sessões, comissões, atos do Executivo.

## T+1 — desfechos

Ver `dados/marcos_institucionais.csv`, filtrando por este ciclo. Atenção às colunas
`canal_demandado` e `canal_efetivo`: a diferença entre elas é o conteúdo empírico da
variável `traducao_institucional`.

## Achado da coleta de 2026-08-22 — a perda do cargo foi *prejudicada*

A Resolução nº 101/1992 do Senado (fonte de nível 1, texto integral recuperado) mostra algo
que o registro não capturava: o pedido de **perda do cargo foi julgado PREJUDICADO** em razão
da renúncia formalizada perante o Congresso, e o processo foi **extinto nessa parte**. O que
a Resolução impõe é apenas a sanção acessória — inabilitação por oito anos para função
pública.

Logo o canal demandado pelo ciclo (impeachment com perda do cargo) não se consumou: o
desfecho efetivo veio da renúncia somada à sanção acessória. `MI-C2-02` passa a
`traducao_institucional = sim`, onde antes constava `nao`.

**Espelho com C4.** Os dois ciclos de impeachment da série produzem desfechos institucionais
inversos quanto à sanção acessória:

| | Perda do cargo | Inabilitação |
|---|---|---|
| **C2 (1992)** | prejudicada pela renúncia | **aplicada** (8 anos) |
| **C4 (2016)** | **aplicada** (61×20) | rejeitada por quórum (42×36×3, exigia 54) |

Essa variação não é captada pelo escore ordinal de `traducao_institucional` em
`cycle_phases.csv`, que registra grau e não direção. É achado a incorporar na discussão de
H1.2 — e um argumento a favor de manter `marcos_institucionais.csv` com `canal_demandado` e
`canal_efetivo` em colunas separadas.

## Predições registradas

<!-- PREDICOES:INICIO — gerado por scripts/renderiza_predicoes.py, não editar à mão -->

**Registradas em 2026-08-22**, antes de qualquer varredura (PROTOCOLO §5). 14 predições: 9 fora de amostra, 5 de âncora, 0 não pertinentes.

O *estatuto probatório* distingue o que pode ser testado do que não pode. Onde a evidência-âncora da hipótese em `docs/quadro-hipoteses.md` vem deste ciclo, a hipótese foi formulada olhando para ele: a predição é reformulação, não previsão, e nenhuma evidência aqui pode refutá-la. Só as predições **fora de amostra** constituem teste.

Fonte de verdade: `dados/predicoes.csv`. Esta seção é gerada — não editar aqui.

### Fora de amostra (9)

*Estas são as predições que podem falhar.*

**H1.3**

- *Predição.* Fora de amostra: a tese classifica a repressão em 1992 como moderada. H1.3 prevê que, sendo moderada, ela NÃO tenha sido o motor da expansão — que deve ser explicada pela DOS (ética na política) e pela vulnerabilidade da elite.
- *O que a refutaria.* Se a maior inflexão de escala do ciclo coincidir com episódio repressivo, e não com marco do processo no Congresso, o motor da expansão é repressivo e H1.3 se aplica onde a tese diz que não se aplica.
- *Teste previsto:* palha ao vento · *Indicador:* Feridos e detidos; variação de participantes antes e depois · *Fonte prevista:* Bancos de eventos; registros institucionais

**H2.1**

- *Predição.* Fora de amostra: a tese descreve cobertura ampla com controle estatal de algumas narrativas. H2.1 prevê que o campo hegemônico discursivo tenha direcionado o desfecho.
- *O que a refutaria.* Se o frame vencedor ('ética na política') tiver origem em atores SEM controle dos meios — movimento estudantil, entidades civis — e ainda assim vencer, a hegemonia dos meios não é o que direciona o ciclo.
- *Teste previsto:* aro · *Indicador:* Enquadramento das revistas semanais; origem social do frame vencedor · *Fonte prevista:* Acervos de imprensa; documentos de entidades

**H2.2**

- *Predição.* Fora de amostra: frame único ('ética na política') e resultado institucional definido em quatro meses. Confirma por contraposição.
- *O que a refutaria.* Multiplicidade de frames incompatíveis documentada em 1992, com resultado ainda assim definido, refutaria a hipótese.
- *Teste previsto:* aro · *Indicador:* Heterogeneidade de demandas nas manifestações · *Fonte prevista:* Bancos de eventos; acervos

**H2.4**

- *Predição.* Fora de amostra: prevê-se que o frame da ética na política tenha lastro discursivo anterior — construído na Constituinte e na campanha de 1989 — e não tenha sido criado em 1992.
- *O que a refutaria.* Frame surgido integralmente durante o ciclo, sem lastro discursivo anterior identificável, refutaria H2.4 neste caso.
- *Teste previsto:* aro · *Indicador:* Cobertura editorial acumulada 1989-1991 · *Fonte prevista:* Acervos de imprensa

**H2.5**

- *Predição.* Fora de amostra: a candidata é a indignação moral legitimada como emoção cívica, expressa no luto encenado do Domingo Negro e no repertório dos caras-pintadas.
- *O que a refutaria.* Repertório emocional idêntico ao de ciclos anteriores, sem legitimação de emoção nova, refutaria a aplicação de H2.5 a este ciclo.
- *Teste previsto:* palha ao vento · *Indicador:* Enquadramentos emocionais; inovação de repertório expressivo · *Fonte prevista:* Acervos; bancos de eventos

**H3.2**

- *Predição.* Fora de amostra: prevê-se leitura conjuntural correta pelos atores do MEP quanto ao timing da pressão sobre o Congresso.
- *O que a refutaria.* Sucesso do ciclo apesar de leitura conjuntural documentadamente equivocada refutaria a ligação entre qualidade da leitura e eficácia.
- *Teste previsto:* aro · *Indicador:* Documentos de deliberação; timing das mobilizações face ao calendário do processo · *Fonte prevista:* Arquivos de entidades estudantis; Diários do Congresso

**H3.3**

- *Predição.* Fora de amostra: candidato bifuncional é o depoimento do motorista Eriberto França na CPMI (jul/1992), que abre simultaneamente a via institucional e a narrativa pública.
- *O que a refutaria.* Aberturas de EOP e DOS em momentos distintos e sem evento comum refutariam a aplicação de H3.3 a este ciclo.
- *Teste previsto:* aro · *Indicador:* Datas de inflexão; marcos da CPMI · *Fonte prevista:* Diários do Congresso; relatório da CPMI

**H3.4**

- *Predição.* Fora de amostra: prevê-se assimetria moderada — o frame da ética na política é apropriável por vários campos, e o legado é de desconfiança difusa, não de clivagem entre campos.
- *O que a refutaria.* Clivagem bipolar documentada como legado de 1992, análoga à de 2013-16, refutaria a gradação que a hipótese pressupõe.
- *Teste previsto:* aro · *Indicador:* Frames disponíveis e proscritos no ciclo seguinte · *Fonte prevista:* Acervos de imprensa

**H3.5**

- *Predição.* Fora de amostra: prevê-se que os legados do Fora Collor — Lei 8.429/1992, normalização do impeachment como instrumento — condicionem ciclos posteriores, ainda que o ciclo seguinte da série esteja a duas décadas de distância.
- *O que a refutaria.* Ausência de qualquer instrumento institucional criado em 1992-93 mobilizado nos ciclos posteriores enfraqueceria a generalidade de H3.5 fora de pares adjacentes.
- *Teste previsto:* aro · *Indicador:* Normas produzidas em 1992-93 e seu uso posterior · *Fonte prevista:* DOU; Diários do Congresso

### Âncora (5)

*Registradas por completude e para o trabalho documental; não testam a hipótese.*

**H1.1**

- *Predição.* Âncora da hipótese: sistema democraticamente aberto pós-CF/1988 viabiliza a mobilização de massa de 1992. Não constitui teste — a proposição foi formulada a partir deste caso.
- *O que a refutaria.* Nada neste ciclo pode refutar H1.1, porque a hipótese foi construída sobre ele. Serve para verificar consistência interna, não para testar.
- *Teste previsto:* palha ao vento · *Indicador:* Pluralismo eleitoral pós-CF/88; acesso de movimentos a arenas institucionais · *Fonte prevista:* Câmara/Senado; TSE

**H1.2**

- *Predição.* Âncora: aprovação de 71% para 9%, deserção parlamentar e inversão midiática precedendo o impeachment. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H1.2. O valor da linha é documental: elevar o placar de 441x38 a fonte de nível 1 no Diário da Câmara.
- *Teste previsto:* palha ao vento · *Indicador:* Série de aprovação presidencial; votação nominal de 29/09/1992 · *Fonte prevista:* Diário da Câmara 30/09/1992, p. 22067

**H1.4**

- *Predição.* Âncora: PT, PDT, CUT e Igreja como aliados. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H1.4.
- *Teste previsto:* palha ao vento · *Indicador:* Partidos e entidades que apoiam publicamente · *Fonte prevista:* Diários do Congresso

**H2.3**

- *Predição.* Âncora: 'ética na política' alinhado ao ethos constituinte de 1988. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H2.3.
- *Teste previsto:* palha ao vento · *Indicador:* Aceitação das demandas em pesquisas; composição das manifestações · *Fonte prevista:* Séries de opinião; bancos de eventos

**H3.1**

- *Predição.* Âncora: este ciclo define o padrão 'convergente' da tipologia. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.1 — os três padrões foram derivados destes casos.
- *Teste previsto:* palha ao vento · *Indicador:* Indicadores combinados de EOP e DOS · *Fonte prevista:* cycle_phases.csv

<!-- PREDICOES:FIM -->
