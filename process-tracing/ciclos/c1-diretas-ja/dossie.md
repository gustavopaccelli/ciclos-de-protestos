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

*A registrar com data ANTES de iniciar a varredura (PROTOCOLO §5). Enquanto esta seção
estiver vazia, qualquer evidência coletada para C1 deve ser tratada como exploratória.*

| Hipótese | Predição | O que a refutaria |
|---|---|---|
| | | |
