# Banco Mass Mobilization (MM) — subconjunto Brasil (1990–2020)

**Autoria:** CLARK, David H. (Binghamton University); REGAN, Patrick M. (Joan Kroc Institute, University of Notre Dame). *Mass Mobilization Protest Data.* Financiamento: Political Instability Task Force.

**Arquivo de origem:** `mmALL_073120` (versão **v16**, 31/07/2020) — cobertura global 162 países, **1990–2020**.
**Distribuição:** Harvard Dataverse (Mass Mobilization Project).

> **Uso neste projeto:** dado de terceiros incorporado para fins de pesquisa acadêmica, com atribuição integral aos autores. **Fonte independente** — não mesclada com os demais bancos (ver `livro-codigo/crosswalk-codigos.md`).

---

## Recorte aplicado

Conforme instrução ("quero somente os dados sobre protestos no Brasil"), foi extraído
**apenas o Brasil** (`country = "Brazil"`, `ccode = 140`) de **todos os anos disponíveis
(1990–2020)**: **224 registros de protesto** (todos com `protest = 1`).

Os arquivos globais originais (CSV de 15 MB e DTA de 29 MB) **não foram versionados** —
por conterem 162 países fora do escopo do projeto. A extração é **reprodutível**:
filtrar o arquivo `mmALL_073120` por `ccode == 140`. O manual/codebook oficial
(`fonte-original/MM_users_manual_0515.pdf`) foi preservado por ser a referência
metodológica essencial.

## Conteúdo da pasta

```
mass-mobilization-clark-regan-2020/
├── README.md                          ← este manifesto
├── fonte-original/
│   └── MM_users_manual_0515.pdf       ← codebook oficial (Clark & Regan 2015)
├── dados/
│   └── protestos_brasil_1990-2020.csv ← 224 registros, 31 colunas (só Brasil)
└── livro-codigo/
    ├── livro-de-codigo.md             ← variáveis + tabelas de código (demandas/respostas)
    └── crosswalk-codigos.md           ← correspondência com códigos do projeto (SEM mesclar)
```

## Distribuição por ano (protestos no Brasil)

| Ano | N | Ano | N | Ano | N |
|---|---|---|---|---|---|
| 1990 | 5 | 2001 | 8 | 2012 | 3 |
| 1991 | 7 | 2002 | 4 | 2013 | **23** |
| 1992 | 4 | 2003 | 8 | 2014 | 9 |
| 1993 | 3 | 2004 | 3 | 2015 | **23** |
| 1994 | 2 | 2005 | 4 | 2016 | **23** |
| 1995 | 6 | 2006 | 4 | 2017 | 8 |
| 1996 | 4 | 2007 | 9 | 2018 | 6 |
| 1997 | 8 | 2008 | 5 | 2019 | 3 |
| 1998 | 11 | 2009 | 3 | 2020 | 1 |
| 1999 | 10 | 2010 | 5 | | |
| 2000 | 9 | 2011 | 3 | | |

Picos em 2013, 2015 e 2016 coincidem com Junho de 2013 e o ciclo do impeachment.
(O baixo N de 2020 reflete o corte da coleta em 07/2020.)

## Proveniência e integridade

- O CSV em `dados/` é uma **extração fiel** (filtro por país) do arquivo `mmALL_073120`,
  sem qualquer alteração de valores. Grafias originais preservadas (inclusive
  `accomodation` com um "m", como no arquivo-fonte).
- Nenhum valor foi imputado, corrigido ou reagrupado.

## Relação com o projeto (três fontes independentes)

| Fonte | Cobertura | Unidade | Fonte primária | Recorte |
|---|---|---|---|---|
| **MM (Clark & Regan)** | 1990–2020 | protesto–país–ano | Imprensa internacional (Lexis-Nexis) | ≥ 50 pessoas, antiestatal |
| **NEPAC (Tatagiba & Galvão)** | 2011–2016 | cidade-evento | Folha de S.Paulo | ≥ 2 pessoas |
| **Pipeline DoCA/BEP** (próprio) | a executar | evento | Acervo Folha | Protocolo BEP-CEBRAP |

As três **não são somáveis** (limiares, fontes e alvos distintos). O uso conjunto é de
**triangulação** — comparar tendências e corroborar picos entre ciclos —, nunca agregação.
O MM oferece a **série temporal mais longa** (desde 1990, cobrindo Fora Collor) e a
dimensão comparada internacional; o NEPAC oferece **microdados nacionais densos** para
2011–2016; o pipeline DoCA produzirá dados sob o Protocolo BEP.

**Referência ABNT sugerida:**

> CLARK, David H.; REGAN, Patrick M. **Mass Mobilization Protest Data.** Harvard Dataverse, v. 16, 2020. Codebook: *Mass Mobilization Data Project — Codebook and User's Manual*, maio 2015.
