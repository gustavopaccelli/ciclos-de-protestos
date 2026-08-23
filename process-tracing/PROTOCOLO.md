# Protocolo do levantamento por process tracing em fontes oficiais

**Versão** 1.0 · **Criado** 2026-08-22 · **Status** ativo

---

## 1. O que este levantamento é, e o que ele não é

É um mapeamento, em **fontes oficiais**, dos quatro ciclos de protesto do projeto,
organizado em três tempos: antecedente (T-1), ciclo (T0) e desfechos (T+1).

**Não** é uma nova análise de eventos de protesto — isso é `pipeline/` + AEP-BEP. Não é uma
nova cronologia — isso é `docs/cronologia-validada.md`, que este protocolo referencia em
vez de duplicar. E não é um substituto dos memorandos de `experiments/`, que permanecem
como material exploratório.

É a **quarta perna** da base probatória do projeto, e a única independente da imprensa:

| Perna | Base | Independência |
|---|---|---|
| `cycle_phases.csv` | codificação ordinal de autor único | — |
| AEP `protest_events` | Acervo Folha | fonte única |
| NEPAC (Tatagiba & Galvão) | Acervo Folha | mesma fonte da anterior |
| Mass Mobilization | imprensa internacional | independente, N pequeno |
| **este levantamento** | **atos oficiais do Estado** | **independente da imprensa** |

## 2. Por que ele existe: três razões extraídas da tese

**2.1 A tese é declaradamente baseada em fontes secundárias.** A seção METODOLOGIA afirma:
"A análise dos dados foi realizada a partir de fontes secundárias, incluindo documentos
históricos, relatórios governamentais, artigos de jornais e literatura acadêmica." Este
levantamento não repete a tese — ele **eleva a base probatória do trabalho anterior** de
secundária para primária.

**2.2 As Diretas Já sustentam a tese teoricamente sem terem sido tratadas empiricamente.**
Os três estudos de caso são Fora Collor, Junho de 2013 e Fora Dilma. Mas o capítulo 2.1
*abre* com as Diretas Já: é de Rodrigues (1993, 1999a, 2001) sobre esse ciclo que a tese
extrai a pergunta fundante — "como conceituar a mobilização política da sociedade em um
contexto de ampliação da arena política?" — e o conceito de *conjunturas fluídas* que
organiza todo o argumento. C1 é, por isso, o caso que mais ganha com este levantamento.

**2.3 O Quadro 8 da tese é o embrião deste trabalho.** Ele cruza nove categorias analíticas
por três ciclos, em formulações qualitativas sem âncora documental peça a peça.
`dados/quadro8_ampliado.csv` o estende ao quarto ciclo e exige, de cada célula, os
`evidencia_id` que a sustentam.

## 3. Estrutura temporal: por que T-1 tem duas camadas

A tese adota as múltiplas temporalidades de Braudel via Vieira (2015): a conjuntura "se
situa entre os fatos de curta duração e as estruturas históricas de longa duração,
representando um recorte temporal de algumas décadas". **Pelos critérios do próprio autor,
uma janela T-1 de 24 meses seria curta demais para capturar conjuntura.** Daí duas camadas
aninhadas:

- **T-1e — antecedente estrutural.** A longa duração do "ciclo de oportunidades políticas
  no Brasil (1970–2015)" que a tese periodiza no cap. 2.2. Indicadores anuais em
  `dados/series_estruturais.csv`.
- **T-1c — antecedente conjuntural.** Janela curta anterior à primeira fase, codificada
  pelas quatro categorias de análise de conjuntura de Herbert José de Souza (1986) que a
  tese adota: acontecimentos, cenários, relações de forças, e articulação entre estrutura
  e conjuntura.

Cada ciclo recebe **duas demarcações simultâneas**, em colunas separadas:

- `janela_fixa` — 24 meses antes da 1ª fase, 24 meses depois do desfecho. Regra mecânica,
  garante comparabilidade. É o padrão da análise.
- `janela_ancorada` — T-1 inicia no desfecho do ciclo anterior; T+1 encerra no ato que
  fecha a disputa.

### 3.1 A janela ancorada não é teste de robustez

É a espinha substantiva do levantamento. O T+1 das Diretas Já não se encerra no Colégio
Eleitoral: alcança a Assembleia Nacional Constituinte, a Constituição de 1988 e, por ela,
a eleição direta de 1989 — sem a qual não há eleição de Collor e portanto não há ciclo
Fora Collor. **O T+1 de C1 é, por construção, o T-1e de C2.**

É isso que torna H3.5 (legados de um ciclo condicionam o seguinte) uma proposição testável
em vez de uma afirmação interpretativa. Operacionalmente: em `marcos_institucionais.csv`
um mesmo marco pode figurar como T+1 de um ciclo e T-1 do próximo, com o **mesmo**
`evidencia_id`, via o campo `ciclo_seguinte_afetado`. Se a cadeia C1→C2 não fecha em fonte
oficial, H3.5 não tem lastro empírico neste levantamento — e o validador diz isso.

## 4. Testes diagnósticos: o que separa isto de uma cronologia comentada

Cada peça de evidência declara, **antes de ser examinada**, o que ela provaria se
encontrada (Van Evera 1997; Beach & Pedersen 2013, já citados em `docs/`):

| Teste | Necessário | Suficiente | Consequência |
|---|:---:|:---:|---|
| Palha ao vento | não | não | ajusta levemente a plausibilidade |
| Aro (*hoop*) | **sim** | não | falhar **elimina** a hipótese; passar não a confirma |
| Arma fumegante | não | **sim** | passar **confirma** fortemente; falhar não elimina |
| Duplamente decisivo | **sim** | **sim** | confirma uma e elimina as rivais. Raro |

O campo `teste_van_evera` é obrigatório. Um levantamento em que tudo é "arma fumegante"
não está fazendo process tracing — está colecionando ilustrações.

## 5. Predições registradas antes da varredura

### O que "predição" significa aqui

Não é prognóstico. A Teoria do Processo Político não é uma teoria preditiva, e o termo
precisa ser definido para não convidar o leitor a cobrar poder preditivo que o desenho não
promete.

Em *Dynamics of Contention* (McAdam, Tarrow e Tilly, 2001), a unidade explicativa é o
**mecanismo**, e o programa é explicitamente contrário à explicação por leis de cobertura:
abandona-se o modelo geral do "movimento social" em favor de mecanismos causais recorrentes
que se compõem em processos, variando de episódio para episódio. Neste protocolo, portanto:

> **Predição = expectativa observável derivada de um mecanismo postulado, registrada com data
> anterior à varredura.** Ela enuncia o que deve aparecer no registro documental *se* o
> mecanismo operou neste episódio. Sua função é diagnóstica, não prognóstica.

Três camadas a sustentam, todas já mobilizadas pelo projeto: o **mecanismo** (McAdam, Tarrow
e Tilly, 2001; Tilly e Tarrow, 2015), de onde a expectativa é derivada; a **fase do ciclo**
(Tarrow), que fornece as regularidades internas ao ciclo — difusão, inovação de repertório,
radicalização e institucionalização — onde vivem as predições por fase; e o **teste
diagnóstico** (Beach e Pedersen, 2013; Van Evera, 1997), que fixa o valor probatório de cada
uma. O valor de uma predição está no teste que ela habilita, não na taxa de acerto.

Dois trabalhos sustentam, de dentro do campo, que aqui não se prevê. Chenoweth e Ulfelder
(2017) testam quatro modelos estruturais de irrupção de levantes não violentos e obtêm, fora
de amostra, resultados mistos para todos eles, recomendando mais ênfase na agência que na
estrutura. Stykow (2022) mostra que nem fatores estruturais nem de agência teriam predito a
mobilização de 2020 em Belarus. São as âncoras de por que as predições deste protocolo são
instrumentos de teste, e não prognósticos.


`experiments/` já usa "predições registradas antes da análise" — a melhor prática do
repositório. Aqui a regra é a mesma e vale por ciclo: **antes** de abrir qualquer fonte
para um ciclo, registrar no dossiê correspondente, com data, o que cada hipótese prevê
encontrar e — mais importante — **o que a refutaria**.

**Cumprido em 2026-08-22.** As 56 predições estão em `dados/predicoes.csv` e renderizadas
nos dossiês por `scripts/renderiza_predicoes.py`. Cada uma traz `o_que_refutaria` — campo
obrigatório: predição cuja refutação não é enunciável em termos de dado observável não é
testável, e o validador acusa.

Cada predição carrega ainda um **estatuto probatório**, porque a anterioridade formal não
basta. As evidências-âncora das 14 hipóteses em `docs/quadro-hipoteses.md` vêm de C2, C3 e
C4; nenhuma vem de C1. Onde a hipótese foi construída a partir do ciclo, a predição é
reformulação — marcada `ancora` e explicitamente não-teste. Só as `fora_de_amostra`
constituem teste, e C1 concentra 14 delas. Assim o viés retrospectivo da §6.4 deixa de ser
ressalva e vira variável registrada.

Alterar uma predição depois de ver evidência exige **nova linha com nova data**,
preservando a anterior — o rastro de auditoria que faltou na recodificação v2→v3.

Corolário operacional: `relacao_com_hipotese` admite `desconfirma`, e o validador conta
desconfirmações por hipótese. **Zero desconfirmação em 14 hipóteses é sinal de viés de
busca, não de força do argumento.**

## 6. Riscos conhecidos e como este protocolo os trata

**6.1 Fonte oficial tem silêncio próprio.** O Diário Oficial registra o que virou ato; não
registra a tentativa fracassada, a articulação informal, a pressão que não virou norma. Por
isso o levantamento pareia DOU com **tramitação legislativa**, que preserva proposições
arquivadas e rejeitadas — e por isso `mecanismo=nao_ocorrencia` é categoria obrigatória.

**6.2 O cão que não latiu.** A própria tese oferece o caso: o Movimento Cansei (2007) teve
pauta antipetista, lideranças e celebridades, mas "não teve grandes articulações, tampouco
conseguiu despontar como um catalisador de grupos". É o contrafactual natural de H2.4 — DOS
construída deliberadamente que **não** pegou. Se H2.4 vale, precisa explicar por que 2007
falha e 2013–2014 funciona. Já está no registro como `desconfirma`.

**6.3 Circularidade no indicador de aprendizado organizacional.** O Quadro 3 mede
"aprendizado organizacional" por contagem de manifestações. Usar aqui o `protest_events` do
próprio projeto e depois usar a mesma série como variável dependente **é circular**. Regra:
para T-1e usar exclusivamente NEPAC e Mass Mobilization; o `protest_events` do projeto fica
reservado ao T0.

**6.4 Viés retrospectivo.** O desfecho de todos os quatro ciclos é conhecido, e as 14
hipóteses foram escritas depois dos fatos. As predições da §5 mitigam, não eliminam. O
dossiê deve declarar isso, e nenhuma hipótese pode ser reformulada *após* ver a evidência
sem que a reformulação fique registrada com data.

**6.5 Quebras de série.** PNAD→PNADC (2012), mudanças de metodologia do IPCA, recontagens
censitárias. Toda quebra vai anotada na linha da série; comparar antes e depois sem
ressalva produz achado espúrio.

**6.6 Não sobrescrever série revisada em silêncio.** Órgãos oficiais revisam dados
retroativamente. `extrai_series_estruturais.py` preserva valor já preenchido salvo
`--forcar`, para que uma revisão do IPCA não mude a base do argumento sem deixar rastro.

## 7. Regra de admissibilidade

Todo marco institucional e toda evidência de T+1 exigem **fonte de nível 1 ou 2** (ver
`fontes/hierarquia-fontes.md`). Imprensa (nível 3) e literatura (nível 4) acompanham,
jamais substituem.

Exceção prevista: evidência de **DOS**, em que o enquadramento midiático *é* o objeto e não
a fonte sobre um terceiro fato. Nesse caso registrar nível 3 com nota explicitando o uso.

## 8. Fluxo de trabalho

1. **Registrar predições** do ciclo no dossiê, com data (§5).
2. **Rodar os extratores** em máquina com rede (`scripts/`), gerando CSV de candidatos.
3. **Classificar manualmente** o que a API não decide: tempo, mecanismo, hipótese vinculada,
   teste diagnóstico. A API estabelece o fato; a inferência é do pesquisador.
4. **Recuperar as fontes de nível 1** para o que ficou em nível 2 — sobretudo os Diários da
   Câmara e do Congresso, que não têm API (caminho em `fontes/registro-fontes.md`).
5. **Rodar `valida_registro.py`** e resolver erros antes de concatenar ao registro.
6. **Atualizar o dossiê** narrativo e as células do Quadro 8 ampliado.

## 9. O que este levantamento não decide

Não altera `cycle_phases.csv`, o quadro de hipóteses, o README nem as seções do artigo. Ele
produz a evidência para revisá-los. A revisão é decisão do pesquisador, em passo separado e
registrada em `research-log.md`.

---

## Referências do protocolo

BEACH, D.; PEDERSEN, R. B. *Process-Tracing Methods*. Michigan, 2013. · CHENOWETH, E.;
ULFELDER, J. Can structural conditions explain the onset of nonviolent uprisings? *JCR*,
2015. · CHRISTIANSEN, J. Four stages of social movements. 2009. · COSTA, G. P. *Estruturas
de mobilização e oportunidades políticas*. Tese (Doutorado) — UFJF, 2024. · JOSÉ DE SOUZA,
H. *Como se faz análise de conjuntura*. Vozes, 1986. · McADAM, D. et al. *Dynamics of
Contention*. 2004. · TILLY, C.; TARROW, S. *Contentious Politics*. 2015. · VAN EVERA, S.
*Guide to Methods for Students of Political Science*. Cornell, 1997. · VIEIRA, 2015.
