# Dossiê C3 — Junho de 2013

**Status** estrutura criada, varredura não iniciada · **Última atualização** 2026-08-22

---

## Estatuto na tese

Estudo de caso empírico de Costa (2024). As formulações do Quadro 8 para este ciclo já
constam de `dados/quadro8_ampliado.csv` na coluna `formulacao_tese_2024` e aguardam
ancoragem em fonte oficial peça a peça — é isso que este dossiê produz.

## Fases

Ver `data/cycle_phases.csv`, prefixo `J13-`. Ciclo de 2013-06-06 a 2013-12-31.

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

## Predições registradas

<!-- PREDICOES:INICIO — gerado por scripts/renderiza_predicoes.py, não editar à mão -->

**Registradas em 2026-08-23**, antes de qualquer varredura (PROTOCOLO §5). 14 predições: 7 fora de amostra, 7 de âncora, 0 não pertinentes.

O *estatuto probatório* distingue o que pode ser testado do que não pode. Onde a evidência-âncora da hipótese em `docs/quadro-hipoteses.md` vem deste ciclo, a hipótese foi formulada olhando para ele: a predição é reformulação, não previsão, e nenhuma evidência aqui pode refutá-la. Só as predições **fora de amostra** constituem teste.

Fonte de verdade: `dados/predicoes.csv`. Esta seção é gerada — não editar aqui.

### Fora de amostra (7)

*Estas são as predições que podem falhar.*

**H1.1**

- *Predição.* Teste severo: a tese registra, via Avritzer, que 2011-2013 foi período de RUPTURA do campo da participação social. Se H1.1 vale, deve-se encontrar abertura institucional preservada apesar dessa ruptura; se o que se encontra é fechamento de canais participativos com mobilização máxima, a relação postulada se inverte.
- *O que a refutaria.* Indicadores oficiais de acesso (conferências nacionais, conselhos ativos, audiências públicas) em queda entre 2011 e 2013, com mobilização atingindo o maior patamar da série, refutam H1.1 na direção proposta.
- *Teste previsto:* aro · *Indicador:* Número de conferências nacionais e conselhos ativos; audiências públicas; acesso de movimentos a arenas federais · *Fonte prevista:* Secretaria-Geral da Presidência; DOU; portais Câmara/Senado

**H1.2**

- *Predição.* Prevê-se magnitude 2 em 19/06/2013 pelo canal demandado (revogação tarifária), seguida de REVERSÃO para 1 a partir de 21/06, com a divisão de elite acumulada travada em 2 — a menor da série. A reversão é o refutador próprio da cláusula da DOS: ela coincide com a queda de od_ressonancia_discursiva de 3 para 1.
- *O que a refutaria.* Se a verificação de MI-C3-01 falhar — isto é, se não houver ato datado de revogação tarifária —, a magnitude 2 em J13-3 perde lastro e a reversão deixa de ser observável. E se o banco de eventos do pipeline DoCA registrar a PEC 37 entre as demandas efetivas do ciclo, cai a codificação nao_demandado_pelo_ciclo, a reversão perde a explicação por substituição de objeto, e a cláusula da DOS fica sem o único caso que a sustenta.
- *Teste previsto:* aro · *Indicador:* Magnitude por fase; od_ressonancia_discursiva entre fases contíguas; ato de revogação · *Fonte prevista:* Prefeitura de São Paulo; Diário da Câmara de 26/06/2013; protest_events

**H1.4**

- *Predição.* Fora de amostra e potencialmente refutador: 2013 é caracterizado como antipartidário, com recusa explícita de bandeiras. H1.4 prevê que a ausência de aliados intrainstitucionais reduza a heterogeneidade da coalizão — mas o observado é heterogeneidade ALTA sem aliados.
- *O que a refutaria.* Coalizão altamente heterogênea documentada em 2013 na ausência de aliados intrainstitucionais refuta H1.4 como enunciada e exige reformulação: aliados podem ampliar, mas não são necessários.
- *Teste previsto:* aro · *Indicador:* Presença ou expulsão de bandeiras partidárias; posição do Judiciário e do MP · *Fonte prevista:* Registros de eventos; manifestações institucionais

**H2.1**

- *Predição.* Fora de amostra: 2013 tem inversão de sinal da cobertura em 48h. H2.1 prevê que, com hegemonia discursiva instável, nenhum campo consiga direcionar o ciclo — o que converge com o resultado 'inacabado'.
- *O que a refutaria.* Direção ideológica clara e sustentada do ciclo de 2013, apesar da instabilidade da cobertura, refutaria a ligação entre hegemonia discursiva e direção.
- *Teste previsto:* aro · *Indicador:* Variação do enquadramento antes e depois de 13/06 · *Fonte prevista:* Acervos de imprensa

**H2.3**

- *Predição.* Fora de amostra: o frame inicial (tarifa) é setorial e de baixa ressonância normativa geral, mas o recrutamento é o maior da série. H2.3 prevê que a ampliação só ocorra APÓS a substituição do frame por um mais ressonante.
- *O que a refutaria.* Recrutamento máximo alcançado ainda sob o frame tarifário, antes da coalescência para pautas amplas, refutaria a relação entre ressonância normativa e amplitude.
- *Teste previsto:* arma fumegante · *Indicador:* Sequência temporal entre mudança de frame e salto de participantes · *Fonte prevista:* protest_events; NEPAC

**H2.4**

- *Predição.* Fora de amostra e potencialmente refutador: se a DOS de 2013 fosse deliberadamente construída, deveria haver rede produtora identificável antes de junho. A tese sugere o contrário — a pulverização de pautas é emergente.
- *O que a refutaria.* Rede de produção discursiva documentada e ativa antes de junho de 2013, com frames que efetivamente dominaram o ciclo, refutaria a leitura de emergência e estenderia H2.4 a um caso que a tese trata como espontâneo.
- *Teste previsto:* arma fumegante · *Indicador:* Atividade de think tanks e redes editoriais 2011-2013 · *Fonte prevista:* Registros dos institutos; acervos

**H3.2**

- *Predição.* Fora de amostra e de alto valor: 2013 é o caso de MENOR eficácia estratégica agregada. H3.2 prevê que isso corresponda a leituras conjunturais pobres ou ausentes — o que a horizontalidade e a recusa de liderança tornam plausível.
- *O que a refutaria.* Leitura conjuntural documentadamente precisa por parte do MPL, seguida de perda de controle do ciclo, mostraria que boa leitura não basta — refutando H3.2 como enunciada.
- *Teste previsto:* arma fumegante · *Indicador:* Documentos e deliberações do MPL e coletivos; timing · *Fonte prevista:* Acervos dos movimentos

### Âncora (7)

*Registradas por completude e para o trabalho documental; não testam a hipótese.*

**H1.3**

- *Predição.* Âncora: repressão de 13/06/2013 seguida de inversão narrativa e salto de 5 mil para 1 milhão. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H1.3. Valor: recuperar em fonte oficial os números de feridos e detidos, hoje sustentados por imprensa.
- *Teste previsto:* palha ao vento · *Indicador:* Feridos/detidos em 13/06/2013; tom da cobertura pós-repressão · *Fonte prevista:* Ouvidoria da Polícia de SP; Defensoria; relatórios oficiais

**H2.2**

- *Predição.* Âncora: coexistência de frames urbanos, anticorrupção, democratizante e moralizador produzindo resultado 'inacabado'. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H2.2.
- *Teste previsto:* palha ao vento · *Indicador:* Número de demandas distintas; ausência de master frame · *Fonte prevista:* protest_events; NEPAC

**H2.5**

- *Predição.* Âncora: a cobertura da repressão legitima a raiva como emoção política. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H2.5.
- *Teste previsto:* palha ao vento · *Indicador:* Enquadramento emocional pós-13/06 · *Fonte prevista:* Acervos de imprensa

**H3.1**

- *Predição.* Âncora: este ciclo define o padrão 'fragmentado' da tipologia. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.1 — os três padrões foram derivados destes casos.
- *Teste previsto:* palha ao vento · *Indicador:* Indicadores combinados de EOP e DOS · *Fonte prevista:* cycle_phases.csv

**H3.3**

- *Predição.* Âncora: 13/06/2013 como evento-catalisador bifuncional. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.3.
- *Teste previsto:* palha ao vento · *Indicador:* Inflexão simultânea de EOP e DOS em 13/06 · *Fonte prevista:* cycle_phases.csv

**H3.4**

- *Predição.* Âncora: 2013 legitima frames antipetistas e deslegitima frames de defesa da democracia, pré-moldando a DOS de 2015-16. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.4.
- *Teste previsto:* palha ao vento · *Indicador:* Análise longitudinal dos enquadramentos antes e depois · *Fonte prevista:* Acervos de imprensa

**H3.5**

- *Predição.* Âncora: o refluxo de junho pré-molda EOP e DOS de 2015-16. Não é teste.
- *O que a refutaria.* Nada neste ciclo refuta H3.5.
- *Teste previsto:* palha ao vento · *Indicador:* Ausência de reforma política; frames herdados · *Fonte prevista:* Diários do Congresso

<!-- PREDICOES:FIM -->
