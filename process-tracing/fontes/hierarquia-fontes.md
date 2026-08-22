# Hierarquia de fontes

Quatro níveis. O nível determina **o que a fonte autoriza afirmar** — não o quanto ela é
confiável em geral.

## Nível 1 — Ato oficial primário

O documento que constitui o ato, publicado pelo órgão que o praticou.

- Diário Oficial da União (Imprensa Nacional)
- Diário da Câmara dos Deputados · Diário do Senado Federal · Diário do Congresso Nacional
- Diários da Assembleia Nacional Constituinte (1987–1988)
- Acórdãos e decisões do STF e do TSE
- Texto legal promulgado (Constituição, leis, emendas, resoluções)
- Resultados eleitorais totalizados pelo TSE
- Séries estatísticas do IBGE e do Banco Central

**Autoriza:** afirmar que o ato ocorreu, em que data, com que conteúdo e que placar.
É o único nível que fecha uma questão sozinho.

## Nível 2 — Registro institucional secundário

A instituição relatando os próprios atos em formato jornalístico ou de acervo.

- Portais de notícias da Câmara, Senado, STF, TSE, Planalto
- Agência Brasil / EBC
- Biblioteca Digital da Câmara · Biblioteca Digital do Senado
- IPEA, DIEESE, Fundação Perseu Abramo, CPDOC/FGV

**Autoriza:** estabelecer marcos institucionais de forma provisória, com obrigação de
elevar a nível 1 quando o documento primário existir. Frequentemente é o nível 2 que
**indica onde está** o nível 1 — o portal da Câmara, por exemplo, linka a página exata do
Diário. Use-o como mapa, não como destino.

## Nível 3 — Imprensa de referência

Jornais e revistas de circulação nacional.

**Autoriza:** corroborar. Nunca estabelecer, sozinho, um marco institucional ou qualquer
elemento do T+1.

**Exceção prevista:** quando o enquadramento midiático *é* o objeto — evidência de DOS, de
visibilidade, de valência — a imprensa deixa de ser fonte sobre um terceiro fato e passa a
ser o próprio dado. Nesse caso registrar `fonte_nivel=3` com nota explicitando o uso. A
distinção importa: "a Folha noticiou que houve 1 milhão" é nível 3 sobre o público; "a
Folha enquadrou o ato como comemoração de aniversário da cidade" é dado primário de DOS.

## Nível 4 — Literatura acadêmica revisada por pares

**Autoriza:** interpretar, contextualizar e localizar fontes de nível 1–2. Não estabelece
fato institucional. A tese de Costa (2024) entra aqui — inclusive porque ela própria se
declara baseada em fontes secundárias.

---

## Fontes de baixo prestígio: por que não há nível 5

`docs/cronologia-validada.md` foi criado para "substituir referências de baixo prestígio
(Terra.com.br, Politize.com.br, Wikipédia)". O objetivo foi cumprido apenas em parte —
naquele documento ainda aparecem "Ensinar História" e "Toda Matéria" sustentando o
Domingo Negro de 16/08/1992, e a InfoEscola circula nas buscas sobre a Emenda Dante de
Oliveira.

Aqui esse material **não tem nível**: não entra no registro em nenhuma hipótese. Se um
fato só existe nessas fontes, ele é `pendente` até ser recuperado em nível 1–3.

## Divergência entre fontes admissíveis

Quando duas fontes de nível 1–2 discordam, o registro **não escolhe em silêncio**. A linha
recebe `status_verificacao=divergencia_nao_resolvida` e o campo `divergencia_entre_fontes`
descreve as duas versões.

Dois casos já no registro:

- **Placar do impeachment de Collor.** O Portal da Câmara registra 441 × 38, 1 abstenção,
  23 ausências. Circula amplamente na web o placar "441 a 33". Resolver pelo Diário da
  Câmara de 30/09/1992, p. 22067.
- **Placar do julgamento de Dilma.** Duas páginas do próprio Senado divergem: a matéria de
  28/12/2016 registra 61 × 20; a página de áudio sobre a sentença registra 61 × 21.
  Resolver pela ata da sessão no Diário do Senado Federal.

Divergência dentro do mesmo órgão é achado sobre a produção do registro oficial, não ruído
a ser descartado.
