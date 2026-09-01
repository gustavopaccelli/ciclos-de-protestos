# Halterman & Keith (2025) — Codebook LLMs

**Referência:** HALTERMAN, Andrew; KEITH, Katherine A. Codebook LLMs: Evaluating LLMs as Measurement Tools for Political Science Concepts. **Political Analysis**, 2024. `[VERIFICAR: coautoria, volume, páginas, DOI]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Argumento central
Cientistas sociais usam codebooks para codificar textos políticos e, cada vez mais,
recorrem a LLMs generativos para isso. Mas há **pouca evidência empírica** de que LLMs
"de prateleira" sigam fielmente as operacionalizações de um codebook real. Os autores
reúnem três codebooks reais — **um deles de eventos de protesto** —, com os textos e
rótulos humanos correspondentes, e propõem um **framework de cinco estágios**. Achado
central: LLMs de peso aberto têm **limitações claras para seguir codebooks em zero-shot**,
mas o ajuste supervisionado por instrução melhora substancialmente o desempenho.

## Conceito/método aproveitável — os cinco estágios
1. Preparar o codebook para leitura por humano **e** por LLM.
2. Testar as capacidades básicas do modelo sobre o codebook.
3. Avaliar a acurácia de medição zero-shot (desempenho "de prateleira").
4. **Analisar os erros** — não apenas contá-los.
5. Treinamento supervisionado (eficiente em parâmetros) quando necessário.

A contribuição declarada dos autores não é apontar o "melhor" LLM, mas oferecer o
framework de avaliação e orientação para quem for implementar medição codebook–LLM
própria. É exatamente o nosso caso.

## Onde entra no projeto
- **`docs/aep-protocol-bep.md` §12** — a seção foi escrita operacionalizando estes cinco
  estágios (§12.1 a §12.5).
- **`pipeline/config/doca_codebook.yaml`** — motivou converter o `actor_schema` de
  comentário YAML para estrutura real (estágio 1: codebook legível por máquina).
- **`pipeline/check_schema_coverage.py`** — o teste existe para garantir o estágio 1.
- **H*** — indiretamente: variáveis com κ insuficiente não podem sustentar teste de hipótese.

## Achado que muda a prática do projeto
A premissa implícita do pipeline atual era que um modelo forte, com o codebook no prompt,
codificaria bem em zero-shot. Este trabalho diz que **não se deve presumir isso** — daí o
gold standard e a análise de erro por tipo terem virado etapas obrigatórias, não opcionais.
