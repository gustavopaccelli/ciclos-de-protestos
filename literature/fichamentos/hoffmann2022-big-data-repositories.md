# Hoffmann et al. (2022) — o véu dos repositórios de big data jornalístico

**Referência:** HOFFMANN, Matthias et al. Lifting the Veil on the Use of Big Data News Repositories: A Documentation and Critical Discussion of A Protest Event Analysis. **Communication Methods and Measures**, 2022. `[VERIFICAR: coautores, volume, número, páginas, DOI]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Argumento central
Big data não é o **ponto de partida** de uma análise; é o **resultado** de uma longa
cadeia de tarefas invisíveis ou semivisíveis, mascaradas pelo que os autores chamam de
"fetiche do tamanho" — a suposição de que volume confere validade. Demonstram isso
documentando a extração de eventos de protesto do **GDELT** em seis países europeus ao
longo de sete anos: para que os dados resistissem a escrutínio científico, foi preciso
coletar dados adicionais, fazer tradução neural em larga escala, análise de conteúdo por
dicionário, classificação por aprendizado de máquina **e codificação humana**.

Conclusão: repositórios "livres e prontos para usar" **não devem ser tomados pelo valor de
face** — exigem recursos substanciais de conhecimento, trabalho, dinheiro e computação.

## Onde entra no projeto
- **`docs/fontes-alternativas.md`** — é a base da recomendação de **não adotar o GDELT como
  fonte primária**, reservando-o, se for o caso, a papel de triangulação explicitamente
  ressalvado.
- **`data/bancos-externos/`** — reforça a regra já vigente no projeto de tratar NEPAC e Mass
  Mobilization como **fontes independentes não somáveis**, cada uma com sua cadeia de
  decisões próprias, em vez de mesclá-las em um "banco maior".
- **`metodologia/relatorio-metodologico.md` §7** — argumento para declarar as decisões de
  processamento como parte das limitações.

## Por que importa aqui especificamente
O projeto tem uma tentação óbvia: o Acervo Folha está bloqueado por credenciais, e o GDELT
é gratuito e cobre 1979–presente. Este trabalho é a razão documentada para não tomar esse
atalho.
