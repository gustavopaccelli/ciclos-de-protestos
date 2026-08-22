# Dossiê C1 — Diretas Já (1983–1985)

**Status** estrutura criada, varredura não iniciada · **Última atualização** 2026-08-22

---

## Por que este é o dossiê prioritário

As Diretas Já sustentam a tese de Costa (2024) **teoricamente** sem terem recebido dela
tratamento empírico sistemático. O capítulo 2.1 abre com Rodrigues (1993, 1999a, 2001)
sobre este ciclo, e é dele que a tese extrai tanto a pergunta central — "como conceituar a
mobilização política da sociedade em um contexto de ampliação da arena política?" — quanto
o conceito de *conjunturas fluídas* que organiza todo o argumento.

O ciclo ocorre sob transição, não sob democracia consolidada, e é precisamente isso que o
torna analiticamente decisivo: é uma articulação entre movimentos sociais, sociedade e
**parte do sistema político** — os partidos de oposição ao regime militar. É o caso que
testa se o triângulo EOP–DOS–conjuntura funciona quando a própria arena está sendo
constituída.

No Quadro 8 ampliado, as **nove células de C1 estão vazias**: a tese não as formulou. Este
dossiê é o que as preenche.

## Fases (de `data/cycle_phases.csv`)

| Fase | Período |
|---|---|
| DJ-0 articulação | 1982-11-15 a 1983-02-28 |
| DJ-1 emergência | 1983-03-01 a 1983-12-31 |
| DJ-2 expansão | 1984-01-01 a 1984-03-31 |
| DJ-3 pico | 1984-04-01 a 1984-04-30 |
| DJ-4 declínio | 1984-05-01 a 1984-12-31 |
| DJ-5 desfecho | 1985-01-01 a 1985-03-31 |

## Janelas

- **janela_fixa** — T-1c: 1980-11-15 a 1982-11-14 · T+1: 1985-04-01 a 1987-03-31
- **janela_ancorada** — T-1c: sem ciclo anterior na série; ancorar na abertura do processo
  de liberalização (a definir com fonte). T+1: **estendido até 1989-12-17**, pelo argumento
  do encadeamento abaixo.

## O encadeamento C1 → C2 é o teste mínimo de H3.5

O T+1 deste ciclo não se encerra no Colégio Eleitoral. A proximidade temporal e causal
liga as Diretas Já à Constituinte e à Constituição de 1988, e por ela às eleições de 1989 —
sem as quais não se compreende a eleição de Collor nem o ciclo Fora Collor. **O T+1 de C1 é,
por construção, o T-1e de C2.**

| Elo | Marco | Data | Status |
|---|---|---|---|
| 0 | Emenda Dante de Oliveira rejeitada (298×65, 3 abst., 113 aus.; exigia 320) | 1984-04-25 | verificado (nível 2) |
| 1 | Colégio Eleitoral elege Tancredo Neves, 480×180, 26 abstenções | 1985-01-15 | verificado (nível 2) |
| 2 | Promulgação da Constituição de 1988 | 1988-10-05 | **pendente** |
| 3 | Eleição direta de 1989; 2º turno elege Collor | 1989-11-15 / 12-17 | **pendente** |

Se essa cadeia não fecha em fonte oficial, H3.5 não tem lastro empírico neste levantamento.
`valida_registro.py` reporta o estado dos elos a cada execução.

## T-1e — antecedente estrutural

A ser preenchido por `scripts/extrai_series_estruturais.py`. Recorte: 1970–1985, dentro do
"ciclo de oportunidades políticas (1970–2015)" do cap. 2.2 da tese.

Atenção específica deste caso: os indicadores do Quadro 3 pressupõem regime competitivo.
Sob autoritarismo em liberalização, `ano_eleitoral` e `democracia` medem coisa diferente do
que medem nos demais ciclos — as eleições de 1982 são o primeiro pleito direto para
governos estaduais desde 1965. Isso não invalida a bateria; exige que a comparação entre
C1 e os demais ciclos declare a diferença de regime em vez de tratá-la como variação de grau.

## T-1c — antecedente conjuntural

Codificar pelas quatro categorias de Souza (1986). Nada preenchido ainda.

| Dimensão | O que buscar | Fonte prevista |
|---|---|---|
| acontecimentos | eleições de 1982; crise da dívida; anistia de 1979 | TSE; DOU; BCB |
| cenários | Congresso, ruas, imprensa sob resquício de censura | Diários do Congresso |
| relações de forças | composição do Congresso; dissidência no PDS | Câmara/Senado |
| articulação estrutura/conjuntura | esgotamento do Estado varguista (Sallum Jr. via tese) | literatura, nível 4 |

## T0 — o ciclo

Cronologia de comícios já validada em `docs/cronologia-validada.md` e em
`data/protest_events_seeds/` (59 eventos-semente) e `data/diretas_ja/` (50 comícios, 490
por estado). **Não reescrever aqui** — referenciar. O que este dossiê acrescenta é o rastro
institucional paralelo: tramitação da PEC, sessões, requerimentos, estado de emergência.

## T+1 — desfechos

Ver a tabela do encadeamento. Nota analítica central: as Diretas Já **perdem a emenda e
vencem o desfecho por outro canal**. É o caso paradigmático de `traducao_institucional`, e
`marcos_institucionais.csv` registra a assimetria em colunas separadas — `canal_demandado`
= eleição direta, `canal_efetivo` = Colégio Eleitoral.

## Predições registradas

<!-- PREDICOES:INICIO — gerado por scripts/renderiza_predicoes.py, não editar à mão -->

**Registradas em 2026-08-22**, antes de qualquer varredura (PROTOCOLO §5). 14 predições: 14 fora de amostra, 0 de âncora, 0 não pertinentes.

O *estatuto probatório* distingue o que pode ser testado do que não pode. Onde a evidência-âncora da hipótese em `docs/quadro-hipoteses.md` vem deste ciclo, a hipótese foi formulada olhando para ele: a predição é reformulação, não previsão, e nenhuma evidência aqui pode refutá-la. Só as predições **fora de amostra** constituem teste.

Fonte de verdade: `dados/predicoes.csv`. Esta seção é gerada — não editar aqui.

### Fora de amostra (14)

*Estas são as predições que podem falhar.*

**H1.1**

- *Predição.* Sob autoritarismo em liberalização, a mobilização multissetorial de 1983-84 deve ser precedida por ampliação MENSURÁVEL de acesso institucional: reforma partidária de 1979 e eleições diretas para governos estaduais em 1982. A escala deve crescer DEPOIS dessas aberturas, não antes.
- *O que a refutaria.* Se a curva de mobilização atingir seu máximo sem que nenhum indicador de acesso institucional tenha se ampliado no biênio anterior, H1.1 confunde condição causal com correlato de época.
- *Teste previsto:* aro · *Indicador:* Reorganização partidária (Lei 6.767/1979); resultados das eleições estaduais de 1982; composição do Congresso · *Fonte prevista:* TSE; Diários do Congresso; DOU

**H1.2**

- *Predição.* Teste fora de amostra decisivo. A vulnerabilidade da elite governante deve ser observável na deserção do PDS (dissidência que origina a Frente Liberal) e preceder o desfecho institucional de jan/1985. ATENÇÃO: o indicador 'aprovação presidencial' não transporta para presidente não eleito diretamente; o teste recai sobre deserção parlamentar.
- *O que a refutaria.* Se o Colégio Eleitoral eleger Tancredo SEM deserção prévia mensurável da base governista — isto é, se a vitória vier apenas de recomposição pós-derrota da emenda —, a vulnerabilidade não antecede o resultado e H1.2 perde poder explicativo no caso fundador.
- *Teste previsto:* arma fumegante · *Indicador:* Número de parlamentares do PDS que migram ou votam com a oposição; votação nominal do Colégio Eleitoral (480x180) · *Fonte prevista:* Diários do Congresso; TSE

**H1.3**

- *Predição.* Teste fora de amostra sob regime autoritário. H1.3 prevê que repressão visível expanda o ciclo. Sob censura residual, a visibilidade é o elo frágil: prevê-se repressão baixa nos grandes comícios (o regime evitou confronto aberto na fase de pico) e, portanto, expansão explicada por outro mecanismo.
- *O que a refutaria.* Se houver episódio repressivo relevante COM cobertura e a mobilização subsequente NÃO crescer, o mecanismo postulado falha no caso em que a repressão era mais provável — refutação forte.
- *Teste previsto:* aro · *Indicador:* Ocorrência de repressão nos comícios de 1984; decretos de emergência; cobertura subsequente · *Fonte prevista:* DOU (medidas de emergência); Diários do Congresso; acervos de imprensa

**H1.4**

- *Predição.* Teste fora de amostra de alto valor: em 1983-84 os aliados intrainstitucionais são partidos de oposição (PMDB), OAB, CNBB e sindicatos — uma coalizão que atravessa Estado e sociedade sob autoritarismo. H1.4 prevê que a heterogeneidade da coalizão acompanhe a entrada desses aliados.
- *O que a refutaria.* Se a heterogeneidade máxima da coalizão for anterior à adesão dos aliados institucionais, os aliados são consequência da mobilização e não sua causa — invertendo a direção postulada.
- *Teste previsto:* arma fumegante · *Indicador:* Manifestações públicas de apoio de OAB, CNBB, partidos; requerimentos e discursos parlamentares · *Fonte prevista:* Diários do Congresso; acervos institucionais de OAB e CNBB

**H2.1**

- *Predição.* Teste fora de amostra: H2.1 prevê que o campo com hegemonia discursiva direcione o ciclo. Em 1984 a grande mídia foi inicialmente reticente (o comício da Sé enquadrado como aniversário de São Paulo) e aderiu tarde. A previsão é que o ciclo NÃO tenha sido direcionado pelo campo hegemônico, e sim contra ele.
- *O que a refutaria.* Se o desfecho institucional de 1985 puder ser atribuído à agenda do campo que controlava a mídia, e não à coalizão oposicionista, H2.1 se sustenta onde se esperava sua falha — e a hipótese perde a capacidade de discriminar casos.
- *Teste previsto:* duplamente decisivo · *Indicador:* Enquadramento dominante na cobertura dos comícios; momento da adesão midiática · *Fonte prevista:* Acervos de imprensa (nível 3, uso declarado como dado de DOS)

**H2.2**

- *Predição.* Fora de amostra: as Diretas Já têm master frame ÚNICO e inequívoco (eleições diretas). H2.2 prevê, por contraposição, resultado institucional definido — e é exatamente o que não ocorre no canal demandado, já que a emenda é derrotada.
- *O que a refutaria.* O caso é o teste mais duro de H2.2: DOS convergente com derrota da demanda. Se H2.2 vale, o resultado por canal alternativo (Colégio Eleitoral) deve contar como 'definido'; se não contar, a hipótese precisa da variável traducao_institucional para sobreviver.
- *Teste previsto:* duplamente decisivo · *Indicador:* Número de demandas distintas; existência de master frame; canal do desfecho · *Fonte prevista:* cycle_phases.csv; marcos_institucionais.csv

**H2.3**

- *Predição.* Teste fora de amostra: H2.3 prevê que frame alinhado a valores normativos dominantes amplie o recrutamento. Em 1984 o frame 'democracia/eleições diretas' deve ter recrutado além das bases orgânicas da oposição — atingindo públicos não mobilizados previamente.
- *O que a refutaria.* Se a composição social dos comícios se restringir às bases já organizadas (sindicatos, estudantes, militância partidária), sem adesão de públicos não-orgânicos, o frame não produziu recrutamento ampliado e H2.3 falha no ciclo de maior escala da série.
- *Teste previsto:* aro · *Indicador:* Composição sociológica dos comícios; adesão de públicos não-orgânicos · *Fonte prevista:* data/diretas_ja/; sementes; literatura

**H2.4**

- *Predição.* Fora de amostra: H2.4 prevê investimento discursivo prévio à abertura da EOP. Em 1983-84 o equivalente funcional dos think tanks são a imprensa alternativa, a Igreja e as entidades de classe. Prevê-se produção discursiva acumulada ANTES de nov/1982.
- *O que a refutaria.* Ausência de produção discursiva organizada anterior à fase de articulação, com o master frame surgindo apenas durante a mobilização, refutaria a necessidade do investimento prévio.
- *Teste previsto:* aro · *Indicador:* Existência e atividade de redes de produção narrativa antes de 1983 · *Fonte prevista:* Acervos da CNBB, OAB, imprensa alternativa

**H2.5**

- *Predição.* Fora de amostra: H2.5 prevê que a transformação nas feeling rules legitime emoções políticas novas. Em 1983-84 a candidata é a passagem do medo à esperança pública — a manifestação massiva como ato emocionalmente permitido após duas décadas de repressão.
- *O que a refutaria.* Se os enquadramentos emocionais da esfera pública permanecerem estáveis ao longo do ciclo, sem deslocamento identificável, a ampliação do repertório discursivo terá outra origem.
- *Teste previsto:* palha ao vento · *Indicador:* Mudança nos enquadramentos emocionais da cobertura; novas categorias de demanda · *Fonte prevista:* Acervos de imprensa (dado de DOS, nível 3 declarado)

**H3.1**

- *Predição.* Único teste fora de amostra de H3.1. A configuração de 1983-84 é EOP restrita (regime autoritário) com DOS convergente (master frame democrático de alta ressonância). H3.1 prevê que essa assimetria produza mobilização de grande escala com resultado institucional NÃO maximizado — que é o observado: recorde de público e derrota da emenda.
- *O que a refutaria.* Se este caso apresentar escala máxima E resultado institucional pleno no canal demandado, a convergência EOP+DOS deixa de ser necessária para a maximização e H3.1 perde poder.
- *Teste previsto:* duplamente decisivo · *Indicador:* Combinação dos indicadores de EOP e DOS por fase em cycle_phases.csv · *Fonte prevista:* cycle_phases.csv; marcos_institucionais.csv

**H3.2**

- *Predição.* Fora de amostra: H3.2 prevê que a qualidade da leitura conjuntural dos atores explique eficácia estratégica. Em 1984 a oposição lê corretamente a abertura mas erra o cálculo do quórum da emenda; e acerta ao migrar para o Colégio Eleitoral. Prevê-se leitura conjuntural documentada nos próprios atores.
- *O que a refutaria.* Ausência de deliberação estratégica documentada — decisões tomadas por inércia ou reação, sem leitura conjuntural registrada — enfraqueceria H3.2 no caso em que a análise de conjuntura era prática corrente dos movimentos.
- *Teste previsto:* aro · *Indicador:* Documentos de deliberação estratégica; timing das decisões · *Fonte prevista:* Arquivos de partidos e entidades; Diários do Congresso

**H3.3**

- *Predição.* Fora de amostra: H3.3 prevê conjuntura crítica onde EOP e DOS se abrem SIMULTANEAMENTE. Candidato em 1984: o comício da Candelária (10/04) ou o do Anhangabaú (16/04), como eventos que abrem visibilidade discursiva e pressão institucional ao mesmo tempo.
- *O que a refutaria.* Se as aberturas de EOP e DOS forem sequenciais e distantes — DOS abrindo meses antes de qualquer inflexão institucional —, o modelo do evento bifuncional não se aplica e H3.3 fica restrita a 2013.
- *Teste previsto:* aro · *Indicador:* Datas de inflexão dos indicadores de EOP e DOS por fase · *Fonte prevista:* cycle_phases.csv; cronologia validada

**H3.4**

- *Predição.* Fora de amostra. Unidade da hipótese: o ciclo como PRODUTOR de assimetria para o seguinte. Prevê-se que as Diretas Já produzam assimetria BAIXA — o frame democrático torna-se consenso, não clivagem — e portanto polarização baixa como legado, contrastando com 2013.
- *O que a refutaria.* Assimetria discursiva alta e polarização documentada como legado de 1984 igualariam este ciclo a 2013 e removeriam a variação que H3.4 precisa para discriminar casos.
- *Teste previsto:* aro · *Indicador:* Frames legitimados e proscritos após 1985; enquadramentos na Constituinte · *Fonte prevista:* Diários da ANC; acervos de imprensa

**H3.5**

- *Predição.* Fora de amostra e ELO CENTRAL do levantamento. Prevê-se que os legados institucionais das Diretas Já — Colégio Eleitoral, Constituinte, CF/1988 e eleição direta de 1989 — condicionem a EOP do Fora Collor, tornando possível tanto a eleição de Collor quanto o instrumento do impeachment previsto na nova Constituição.
- *O que a refutaria.* Se a EOP de 1992 puder ser explicada sem referência aos legados de 1985-1989 — isto é, se os instrumentos mobilizados em 1992 forem anteriores ou independentes da CF/88 —, a cadeia postulada se rompe e H3.5 perde seu caso mais forte.
- *Teste previsto:* duplamente decisivo · *Indicador:* Dispositivos da CF/88 mobilizados em 1992; cadeia MI-C1-03 e MI-C1-04 · *Fonte prevista:* Texto da CF/1988; Diários da ANC; TSE

<!-- PREDICOES:FIM -->
