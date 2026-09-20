# Dossiê C4 — Impeachment de Dilma Rousseff (2014–2016)

**Status** estrutura criada, varredura não iniciada · **Última atualização** 2026-08-22

---

## Estatuto na tese

Estudo de caso empírico de Costa (2024). As formulações do Quadro 8 para este ciclo já
constam de `dados/quadro8_ampliado.csv` na coluna `formulacao_tese_2024` e aguardam
ancoragem em fonte oficial peça a peça — é isso que este dossiê produz.

## Fases

Ver `data/cycle_phases.csv`, prefixo `ID-`. Ciclo de 2014-10-27 a 2016-09-30.

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

## Achado da coleta de 2026-08-22 — duas votações, não uma

A divergência registrada em `EV-C4-T1-001` (61×20 numa página do Senado, 61×21 em outra)
está **resolvida**: houve duas votações distintas na sessão de 31/08/2016, separadas por
decisão do presidente do STF, que presidia o julgamento.

| Votação | Resultado | Quórum | Desfecho |
|---|---|---|---|
| Condenação e perda do mandato | 61 × 20 | 2/3 = 54 | aprovada |
| Inabilitação para função pública | 42 × 36, 3 abstenções | maioria absoluta = 54 | **rejeitada** |

O placar de 21 contrários, presente numa página de áudio do Senado, é inconsistente com as
demais páginas oficiais.

**Espelho com C2.** Em 1992 a perda do cargo foi prejudicada pela renúncia mas a inabilitação
foi aplicada; em 2016 a perda do cargo foi aplicada mas a inabilitação falhou por quórum. Os
dois ciclos de impeachment da série produzem desfechos **inversos** quanto à sanção
acessória — variação que o escore ordinal de `traducao_institucional` não captura.

## Predições registradas

<!-- PREDICOES:INICIO — gerado por scripts/renderiza_predicoes.py, não editar à mão -->

**Registradas em 2026-08-23**, antes de qualquer varredura (PROTOCOLO §5). 14 predições: 6 fora de amostra, 6 de âncora, 2 não pertinentes.

O *estatuto probatório* distingue o que pode ser testado do que não pode. Onde a evidência-âncora da hipótese em `docs/quadro-hipoteses.md` vem deste ciclo, a hipótese foi formulada olhando para ele: a predição é reformulação, não previsão, e nenhuma evidência aqui pode refutá-la. Só as predições **fora de amostra** constituem teste.

Fonte de verdade: `dados/predicoes.csv`. Esta seção é gerada — não editar aqui.

### Fora de amostra (6)

*Estas são as predições que podem falhar.*

**H1.1**

- *Predição.* Sistema aberto e competitivo, com eleição presidencial recém-disputada em 2014. H1.1 prevê mobilização multissetorial ampla — o que se observa. O teste está em distinguir efeito de abertura de efeito de polarização.
- *O que a refutaria.* Se a composição setorial da mobilização de 2015-16 for MENOS heterogênea que a de 1992, apesar de abertura institucional igual ou maior, a abertura não explica a multissetorialidade.
- *Teste previsto:* palha ao vento · *Indicador:* Fragmentação de elites; índice de pluralismo eleitoral; composição setorial das coalizões · *Fonte prevista:* TSE; Câmara/Senado

**H1.3**

- *Predição.* Fora de amostra: a tese classifica a repressão em 2015-16 como contida. H1.3 prevê ausência de expansão por via repressiva e, por simetria, prevê que a repressão contida decorra do alinhamento entre manifestantes e aliados no aparato estatal.
- *O que a refutaria.* Repressão significativa documentada em 2015-16 contra manifestações pró-impeachment, sem efeito de expansão, refutaria a leitura de que a contenção é função do alinhamento político.
- *Teste previsto:* aro · *Indicador:* Registros de intervenção policial; feridos/detidos · *Fonte prevista:* Secretarias estaduais de segurança; Anuário FBSP

**H2.2**

- *Predição.* Fora de amostra: frame convergente (anticorrupção antipetista) e resultado definido. Confirma por contraposição.
- *O que a refutaria.* Fragmentação de frames documentada em 2015-16 com resultado ainda assim definido refutaria H2.2.
- *Teste previsto:* aro · *Indicador:* Heterogeneidade ideológica dos participantes · *Fonte prevista:* NEPAC; bancos de eventos

**H2.3**

- *Predição.* Fora de amostra: 'anticorrupção' é frame de alta ressonância normativa. H2.3 prevê recrutamento amplo e socialmente heterogêneo.
- *O que a refutaria.* Recrutamento concentrado em estrato socioeconômico único, apesar da alta ressonância declarada do frame, refutaria a ligação entre ressonância e amplitude social.
- *Teste previsto:* aro · *Indicador:* Composição sociológica das manifestações de 2015-16 · *Fonte prevista:* NEPAC; levantamentos de perfil

**H2.5**

- *Predição.* Fora de amostra: a candidata é a legitimação do desprezo e da hostilidade partidária como expressão cívica aceitável. H2.5 prevê deslocamento observável nos enquadramentos emocionais entre 2013 e 2015.
- *O que a refutaria.* Continuidade dos enquadramentos emocionais entre 2013 e 2015-16, sem deslocamento, enfraqueceria tanto H2.5 quanto H3.4.
- *Teste previsto:* aro · *Indicador:* Comparação longitudinal dos enquadramentos emocionais · *Fonte prevista:* Acervos de imprensa

**H3.3**

- *Predição.* Fora de amostra: candidato bifuncional é a divulgação dos áudios em 16/03/2016 ou a admissibilidade em 17/04/2016. H3.3 prevê que o pico da mobilização seja imediatamente posterior a um desses.
- *O que a refutaria.* Pico de mobilização desconectado de qualquer evento que abra EOP e DOS ao mesmo tempo refutaria H3.3 neste ciclo.
- *Teste previsto:* aro · *Indicador:* Datas de inflexão; decisões do STF · *Fonte prevista:* Diários; decisões do STF

### Âncora (6)

*Registradas por completude e para o trabalho documental; não testam a hipótese.*

**H1.2**

- *Predição.* Âncora: crise econômica, Lava Jato e deserção do PMDB precedendo a admissibilidade de 17/04/2016. Não é teste. Observação intracaso a registrar como mecanismo = nao_ocorrencia: entre março e dezembro de 2015 (ID-1 e ID-2) op_divisao_elites vale 3 e a magnitude permanece 0 por oito meses; o teto só sobe quando o canal abre, em 02/12/2015.
- *O que a refutaria.* Nada neste ciclo refuta H1.2. Valor documental ampliado: além da divergência de placar já resolvida, verificar no Diário do Senado a qualificação do limiar de 54 na votação da inabilitação — o registro do repositório dizia 'maioria absoluta', corrigido em 2026-08-23 para dois terços de 81.
- *Teste previsto:* palha ao vento · *Indicador:* Datas de abertura do canal; deserção do PMDB em 29/03/2016; margens das duas votações · *Fonte prevista:* Diário do Senado de 31/08/2016; notas taquigráficas de 17/04/2016

**H1.4**

- *Predição.* Âncora: Judiciário/Lava Jato, empresariado, PMDB e mídia hegemônica. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H1.4.
- *Teste previsto:* palha ao vento · *Indicador:* Posição do Judiciário; adesão empresarial · *Fonte prevista:* Decisões do STF; registros institucionais

**H2.1**

- *Predição.* Âncora: Veja, Globo e think tanks liberais produzindo DOS antipetista hegemônica. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H2.1.
- *Teste previsto:* palha ao vento · *Indicador:* Análise de conteúdo da cobertura; presença de think tanks · *Fonte prevista:* Acervos de imprensa; registros dos institutos

**H2.4**

- *Predição.* Âncora: Instituto Millenium, Instituto Liberal, Veja e Globo construindo DOS antipetista em 2013-2014. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H2.4. O contrafactual está registrado à parte: o Movimento Cansei (2007) é construção deliberada que NÃO pegou (EV-C4-T1-002).
- *Teste previsto:* palha ao vento · *Indicador:* Financiamento e atividade das redes; cobertura acumulada · *Fonte prevista:* Registros dos institutos

**H3.1**

- *Predição.* Âncora: este ciclo define o padrão 'construção deliberada' da tipologia. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.1 — os três padrões foram derivados destes casos.
- *Teste previsto:* palha ao vento · *Indicador:* Indicadores combinados de EOP e DOS · *Fonte prevista:* cycle_phases.csv

**H3.2**

- *Predição.* Âncora: MBL e Vem Pra Rua leem corretamente; a esquerda lê tarde. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.2.
- *Teste previsto:* palha ao vento · *Indicador:* Comparação retrospectiva das leituras; timing das decisões · *Fonte prevista:* Acervos dos movimentos

### Não pertinente ao desenho (2)


**H3.4**

- *Predição.* NÃO PERTINENTE ao desenho de quatro ciclos: H3.4 mede o legado de um ciclo sobre o SEGUINTE, e o ciclo do impeachment é o último da série. Avaliar seu legado exigiria incorporar 2018 em diante, o que está fora do recorte.
- *O que a refutaria.* Não se aplica. Registrar como limite declarado do desenho, não como omissão.
- *Teste previsto:* nan · *Indicador:* — · *Fonte prevista:* —

**H3.5**

- *Predição.* NÃO PERTINENTE ao desenho de quatro ciclos: sendo o último ciclo da série, não há ciclo subsequente dentro do recorte sobre o qual medir o condicionamento.
- *O que a refutaria.* Não se aplica. Limite declarado do desenho.
- *Teste previsto:* nan · *Indicador:* — · *Fonte prevista:* —

<!-- PREDICOES:FIM -->
