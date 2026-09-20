# Haunss et al. (2025) — PAPEA: pipeline modular para automação da AEP

**Referência:** HAUNSS, Sebastian et al. PAPEA: A modular pipeline for the automation of protest event analysis. **Political Science Research and Methods**, 2025. `[VERIFICAR: coautores, volume, páginas, DOI]`
**Nível de leitura:** abstract (levantamento 2026-07-18). Não lido na íntegra.

## Argumento central
LLMs podem automatizar a classificação de eventos de protesto — e de dados de eventos
políticos em geral — com **acurácia comparável à humana**, reduzindo o tempo de anotação
em várias ordens de grandeza. Os autores propõem um pipeline **modular** (PAPEA) baseado
em LLMs afinados (*fine-tuned*), com modelos e ferramentas publicamente disponíveis,
demonstrado sobre um grande corpus jornalístico alemão.

## Conceito/método aproveitável
1. **Modularidade por tarefa.** O pipeline separa as tarefas em módulos independentes em
   vez de pedir tudo em uma chamada. Isso é diretamente relevante: nosso
   `02_doca_coder.py` faz triagem e codificação **em uma única passagem**, contrariando o
   §11 do nosso próprio protocolo, que as descreve como Passagens 2 e 3 distintas.
2. **Fine-tuning como caminho de melhoria**, não apenas prompt engineering — incorporado
   como estágio 5 da escalada do protocolo §12.5.
3. Publicação de modelos e ferramentas como parte do desenho — padrão de
   reprodutibilidade a perseguir.

## Onde entra no projeto
- **`docs/aep-protocol-bep.md` §12** — referência de desenho, ao lado de Halterman & Keith.
- **`pipeline/`** — argumento para separar triagem e codificação em duas passagens; hoje
  estão fundidas (defeito conhecido, ainda não corrigido).
- **`metodologia/relatorio-metodologico.md` §4.1** — legitima metodologicamente a opção por
  codificação assistida por LLM, hoje sustentada apenas por Alonso et al. (2024, p. 320).

## Ressalva
O caso demonstrado é um corpus **alemão**. A transposição para português brasileiro, e
sobretudo para texto de 1983–1992 vindo de OCR, não é automática — reforça a necessidade
do gold standard estratificado por ciclo (§12.3).
