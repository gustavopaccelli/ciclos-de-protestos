# Registro de fontes oficiais — caminho de busca

Onde procurar, com o caminho exato. Verificado em 2026-08-22 quanto à existência dos
repositórios; a recuperação dos documentos exige máquina com acesso à internet.

---

## Câmara dos Deputados

**Dados abertos (API v2)** — `https://dadosabertos.camara.leg.br/api/v2`
Proposições, tramitação, votações nominais, órgãos, CPIs. Automatizado em
`scripts/extrai_camara_senado.py`.
*Limite:* cobertura sólida no período recente; para 1983–1992 as proposições existem mas
as votações nominais frequentemente não.

**Diários digitalizados** — `https://imagem.camara.gov.br`
É a fonte de **nível 1** para C1 e C2, e **não tem API**. Recuperação manual pelo padrão:
`dc_20.asp?selCodColecaoCsv={D|J}&txPagina={pagina}&Datain={dd/mm/aaaa}`
onde `D` = Diário da Câmara e `J` = Diário do Congresso.
Âncoras já identificadas:
- Votação do impeachment de Collor → `D`, p. 22067, `30/09/1992`
- Sessão de discussão do parecer → `D`, p. 22009, `29/09/1992`
- Abertura do julgamento no Senado → `J`, p. 4811, `30/12/1992`

**Biblioteca Digital** — `https://bd.camara.leg.br`
Monografias e estudos da Consultoria Legislativa. Foi por ela que se recuperou o placar da
PEC 37. Nível 2, mas frequentemente cita o nível 1.

## Senado Federal

**Dados abertos** — `https://legis.senado.leg.br/dadosabertos`
Matérias, tramitação, votações.
**Diário do Senado** — `https://www25.senado.leg.br/web/atividade/diarios`
Fonte de nível 1 para a ata do julgamento de 31/08/2016, necessária para resolver a
divergência 61×20 / 61×21.
**Legislação** — Resolução nº 101/1992 (sanções no processo contra Collor).

## Imprensa Nacional / DOU

`https://www.in.gov.br` — busca por data e por seção. Sem API pública estável; a busca
`leiturajornal?data=dd-mm-aaaa` devolve a edição do dia.
Uso previsto: promulgação da CF/88, decretos e medidas provisórias das janelas T+1.

## Assembleia Nacional Constituinte (1987–1988)

`https://www.camara.leg.br/internet/constituicao20anos/` e o acervo de Diários da ANC.
Elo 2 da cadeia C1→C2. Nível 1.

## TSE

`https://www.tse.jus.br` — jurisprudência e julgados históricos; repositório de dados
eleitorais para totalizações. Fontes para o Colégio Eleitoral de 1985 e a eleição de 1989
(elos 1 e 3 da cadeia C1→C2), e para o indicador `ano_eleitoral`.

## STF

`https://portal.stf.jus.br` — acórdãos. Relevante para C4 (ADPF/MS sobre o rito do
impeachment) e para o mandado de segurança sobre o rito em 1992.

## IBGE

`https://servicodados.ibge.gov.br/api/v3/agregados` (API) e `https://sidra.ibge.gov.br`.
Agregados usados: 1737 (IPCA), 6784 (Contas Nacionais), 202/6579 (população e urbanização),
7358 (projeções por idade), PNAD/PNADC (escolaridade).
*Atenção:* a transição PNAD→PNADC em 2012 quebra a série de escolaridade.

## Banco Central

`https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json`
Série 433 = IPCA mensal. Automatizado em `scripts/extrai_series_estruturais.py`.

## DIEESE

`https://www.dieese.org.br` — Sistema de Acompanhamento de Greves. Nível 2. É o único
caminho viável para o indicador de capacidade organizacional; não há série oficial
governamental equivalente para a série longa.

---

## Lacunas sem fonte oficial brasileira

Registradas para que não sejam preenchidas com proxy improvisado:

- **Índice de integridade física / repressão.** O Quadro 3 usa o CIRI. Não há equivalente
  oficial brasileiro para a série longa. Alternativa: codificar resposta estatal no próprio
  `protest_events` (Bloco V do AEP-BEP) e complementar com o Anuário do FBSP (nível 2) para
  o período recente. A lacuna fica declarada, não tapada.
- **Índice de democracia.** Polity e V-Dem são produção acadêmica internacional, nível 4 por
  definição. Manter como tal, marcados.
