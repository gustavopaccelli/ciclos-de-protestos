# Bancos de dados externos

Esta pasta reúne **bancos de dados de terceiros** incorporados ao projeto para fins de
pesquisa acadêmica, mantidos separados dos dados produzidos internamente
(`data/cycle_phases.csv`, pipeline AEP em `pipeline/`).

## Princípio de organização

Cada banco externo ocupa uma **subpasta própria**, nomeada por
`fonte-autores-ano`, com a seguinte estrutura padrão:

```
<fonte-autores-ano>/
├── README.md            ← manifesto: autoria, proveniência, estrutura, licença, relação com o projeto
├── fonte-original/      ← arquivos originais preservados sem alteração (auditoria)
├── dados/               ← versões versionáveis (CSV UTF-8, datas ISO 8601)
└── livro-codigo/        ← livro de código / documentação metodológica
```

## Regras

1. **Preservar o original**: os arquivos em `fonte-original/` nunca são editados.
2. **Conversões documentadas**: qualquer transformação (formato, encoding, datas)
   é registrada no README da subpasta; nenhum valor substantivo é alterado ou imputado.
3. **Proveniência e atribuição**: cada README identifica autores, portal de origem,
   fonte primária e a referência ABNT correta para citação.
4. **Sem credenciais**: nenhum arquivo desta árvore deve conter chaves, senhas ou
   dados de acesso (ver `.gitignore` / regra do `.env`).

## Bancos incorporados

| Subpasta | Fonte | Cobertura | Registros (Brasil) |
|---|---|---|---|
| `nepac-tatagiba-galvao-2019/` | Tatagiba & Galvão (NEPAC/CEMARX-UNICAMP) — Protestos no Brasil em tempos de crise | 2011–2016 | 2.548 registros / 1.284 eventos |
| `mass-mobilization-clark-regan-2020/` | Clark & Regan — Mass Mobilization Protest Data (v16) | 1990–2020 | 224 protestos (só Brasil, ccode 140) |

> **Importante:** os bancos são **fontes independentes** e **não somáveis** entre si
> (limiares de inclusão, fontes primárias e definições de alvo distintos). O uso conjunto
> é de **triangulação**, não de agregação. Cada subpasta traz seu próprio livro de código;
> o banco MM inclui ainda um `crosswalk-codigos.md` que relaciona (sem mesclar) suas
> categorias aos códigos do projeto.
