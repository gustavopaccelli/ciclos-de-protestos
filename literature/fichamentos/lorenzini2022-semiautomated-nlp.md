# Lorenzini et al. (2022) — AEP semiautomatizada com NLP

**Referência:** LORENZINI, Jasmine et al. Protest Event Analysis: Developing a Semiautomated NLP Approach. **American Behavioral Scientist**, 2021. `[VERIFICAR: coautoria, volume, número, páginas, DOI]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Argumento central
A codificação manual de eventos de protesto é cara e lenta; abordagens automatizadas
permitem cobrir múltiplas fontes e criar bases grandes em muitos países e anos. Mas —
argumento central — **os procedimentos raramente são descritos em detalhe**, o que impede
avaliar validade e confiabilidade dos dados. Os autores descrevem detalhadamente seu
desenho semiautomatizado e discutem extensamente os **vieses** associados a estudar
protestos a partir do noticiário.

Trabalho companheiro (LORENZINI et al., 2020) descreve a operação em escala: 5 milhões de
documentos triados automaticamente, anotação manual para precisão na codificação de
formas, atores e temas, resultando em **30.000 eventos únicos em 30 países europeus**.

## Conceito/método aproveitável
- **Divisão de trabalho semiautomatizada:** NLP para *identificar documentos relevantes* em
  massa; anotação manual para *codificar com precisão* forma, ator e tema. Não é
  automatizar tudo — é automatizar a triagem, que é onde o volume está.
- **Obrigação de documentar o procedimento** como condição de avaliabilidade dos dados.
  É a justificativa direta para o §12.6 (registro obrigatório) do nosso protocolo.

## Onde entra no projeto
- **`docs/aep-protocol-bep.md` §12.4 e §12.6** — tipologia de erro e registro de execução.
- **`docs/fontes-alternativas.md`** — o argumento de viés de fonte única sustenta a busca
  por fontes múltiplas na Hemeroteca Digital para Diretas Já e Fora Collor.
- **`metodologia/relatorio-metodologico.md` §7 (limitações)** — o viés de cobertura
  jornalística precisa ser declarado, não apenas mitigado.

## Tensão produtiva com o desenho atual
Lorenzini et al. mantêm a **codificação** manual e automatizam só a triagem. Nosso pipeline
automatiza ambas. Haunss et al. (2025) sustentam que hoje é viável automatizar mais — mas a
divergência entre os dois desenhos é justamente o que o gold standard (§12.3) precisa
arbitrar empiricamente, em vez de decidir por preferência.
