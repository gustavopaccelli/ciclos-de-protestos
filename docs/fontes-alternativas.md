# Fontes alternativas ao Acervo Folha — parecer

Data: 2026-07-18. Frente D (pipeline AEP).

## O problema

O pipeline `pipeline/` depende do **Acervo Folha**, que exige assinatura pessoal paga
(`FOLHA_EMAIL` / `FOLHA_PASSWORD` em `.env`). Enquanto não houver credenciais, a coleta não
roda — e os seletores CSS de `01_scraper.py` sequer podem ser validados, porque não há como
inspecionar o site logado. É o gargalo declarado em `metodologia/relatorio-metodologico.md` §7.

Há um segundo problema, independente do primeiro e mais grave para o desenho comparativo:
**os bancos externos não cobrem os dois primeiros ciclos.**

| Ciclo | NEPAC (2011–2016) | Mass Mobilization (1990–2020) | Cobertura efetiva |
|---|---|---|---|
| Diretas Já (1982–85) | não | não | apenas o seed manual (59 eventos) |
| Fora Collor (1991–92) | não | sim, parcial | seed manual (15 eventos) + MM |
| Junho 2013 | sim | sim | densa |
| Impeachment (2014–16) | sim | sim | densa |

Ou seja: mesmo com credenciais da Folha, a assimetria de cobertura entre os ciclos antigos e
os recentes permaneceria. Uma fonte alternativa que cubra 1982–1992 tem valor **independente**
de destravar o Acervo.

## Avaliação das alternativas

### 1. Hemeroteca Digital Brasileira (Biblioteca Nacional) — **prioridade alta**

- **Cobertura:** periódicos brasileiros digitalizados, incluindo décadas de 1980–90. É a única
  alternativa aqui que ataca diretamente a lacuna Diretas Já / Fora Collor.
- **Acesso:** público e gratuito, sem assinatura.
- **Vantagem adicional:** permite **múltiplas fontes** (não só um jornal), o que responde ao
  problema clássico de viés de seleção por fonte única (Earl et al. 2004) — hoje o desenho se
  apoia no argumento de 92% de concordância Folha/Estadão em 2013 (§1 do protocolo), que não
  se pode presumir válido para 1984.
- **Custos:** texto proveniente de **OCR de material impresso antigo**, com qualidade variável.
  Isso afeta diretamente a codificação: nomes de organizações e números de público são
  justamente o que o OCR mais erra. Exigiria um estágio de limpeza antes da Passagem 2 e uma
  taxa de amostragem manual maior no gold standard (§12.3).
- **A verificar:** existência e estabilidade de acesso programático (API ou padrão de URL),
  termos de uso quanto a coleta automatizada, e cobertura efetiva por título/ano.

### 2. GDELT — **prioridade baixa, com ressalva metodológica forte**

- **Cobertura:** 1979–presente, global, acesso livre via BigQuery/arquivos.
- **Ressalva decisiva:** Hoffmann et al. (2022, *Communication Methods and Measures*)
  documentam em detalhe que repositórios de "big data" jornalístico como o GDELT **não são
  prontos para uso**: exigem tradução, reclassificação e codificação humana adicionais, e a
  aparência de exaustividade mascara decisões opacas de processamento. Usar GDELT como fonte
  primária contradiria o rigor que o Protocolo BEP impõe ao resto do desenho.
- **Uso defensável:** apenas como **terceira fonte de triangulação** para os ciclos recentes,
  jamais como substituto do AEP próprio, e sempre com a ressalva registrada.

### 3. GLOCON — **a verificar antes de decidir**

- Base de eventos contenciosos extraídos automaticamente de fontes nacionais em múltiplos
  idiomas (Yörük et al.), com corpus gold standard e manuais de anotação publicados.
- **Interesse principal não é o dado, é o método:** os *annotation manuals* do GLOCON são um
  modelo maduro de gold standard multilíngue, diretamente aproveitável no §12.3 — inclusive
  para um contexto não-anglófono, que é o nosso caso.
- **A verificar:** se há cobertura de fontes brasileiras. Sem isso, o valor é metodológico e
  não empírico.

### 4. Acervos institucionais de acesso aberto — **complementar, já em uso**

Agência Brasil/EBC, Câmara, Senado, CPDOC/FGV, Fundação Perseu Abramo. Já empregados em
`docs/cronologia-validada.md` para validação de cronologia. **Não servem para AEP** — não são
cobertura jornalística sistemática e diária, e produziriam uma série com viés institucional
severo. Mantêm o papel atual: verificação pontual de datas e fatos, não contagem de eventos.

## Recomendação

1. **Investigar a Hemeroteca Digital** como fonte para Diretas Já e Fora Collor, em desenho
   separado do scraper da Folha (fonte com estrutura, licença e qualidade de texto distintas —
   um `01b_scraper_hemeroteca.py`, não um parâmetro do existente).
2. **Não adotar GDELT** como fonte primária; reservá-lo, se for o caso, a papel de triangulação
   explícito e ressalvado.
3. **Ler os manuais de anotação do GLOCON** para o desenho do gold standard do §12.3,
   independentemente de haver ou não cobertura brasileira.
4. **Manter o Acervo Folha** como fonte primária dos ciclos recentes quando houver credenciais
   — ele continua sendo a melhor série contínua e é a fonte do BEP e do NEPAC, o que preserva
   a comparabilidade com esses bancos.

> **Status:** parecer, não decisão executada. Nenhuma coleta foi realizada. Os itens marcados
> "a verificar" dependem de consulta às fontes, ainda não feita — não devem ser tratados como
> confirmados.
