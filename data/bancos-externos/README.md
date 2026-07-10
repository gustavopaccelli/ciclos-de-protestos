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

| Subpasta | Fonte | Cobertura | Registros |
|---|---|---|---|
| `nepac-tatagiba-galvao-2019/` | Tatagiba & Galvão (NEPAC/CEMARX-UNICAMP) — Protestos no Brasil em tempos de crise | 2011–2016 | 2.548 registros / 1.284 eventos |
