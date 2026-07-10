# Banco NEPAC/UNICAMP — Protestos no Brasil (2011–2016)

**Autoria:** TATAGIBA, Luciana; GALVÃO, Andreia (coord.). *Os protestos no Brasil em tempos de crise (2011-2016).* Pesquisa "Confronto político no Brasil, da ascensão à crise dos governos petistas (2003-2016)". NEPAC / CEMARX — Departamento de Ciência Política, UNICAMP, 2019.

**Portal de origem:** https://nepac.ifch.unicamp.br/banco-de-dados
**Fonte primária dos eventos:** Acervo Folha de S.Paulo (cadernos Poder, Mercado, Cotidiano).

> **Uso neste projeto:** dado de terceiros incorporado para fins de pesquisa acadêmica, com atribuição integral aos autores. Não modificamos o conteúdo substantivo. Ver seção "Proveniência e integridade" abaixo.

---

## Conteúdo da pasta

```
nepac-tatagiba-galvao-2019/
├── README.md                       ← este arquivo (manifesto)
├── fonte-original/                 ← arquivos originais preservados, sem alteração
│   ├── protestos_no_brasil_2011-2016.xlsx
│   └── tatagiba_galvao_2019_livro_de_codigo.docx
├── dados/
│   └── protestos_2011-2016.csv     ← XLSX convertido p/ CSV UTF-8 (datas em ISO 8601)
└── livro-codigo/
    └── livro-de-codigo.md          ← livro de código transcrito em Markdown
```

## Estrutura dos dados

- **Unidade de registro:** linha cidade-evento (a Tabela Específica do banco original).
- **2.548 registros** correspondentes a **1.284 eventos únicos** (`Codigo_evento`).
- Um mesmo evento em várias cidades compartilha o mesmo `Codigo_evento` — permite análise **agregada por evento** ou **desagregada por cidade** (ver livro de código, "Evento único vs. eventos distintos").

### Distribuição por ano (data de início)

| Ano | Registros |
|---|---|
| 2011 | 209 |
| 2012 | 407 |
| 2013 | 729 |
| 2014 | 268 |
| 2015 | 454 |
| 2016 | 481 |

O pico de 2013 (Junho) e a alta de 2015–2016 (impeachment) coincidem com dois dos quatro ciclos do projeto.

### Dicionário de colunas (27 variáveis)

| Coluna | Descrição |
|---|---|
| `Identificacao_do_veiculo` | Chave primária da notícia (`Ano+Mês+Dia+FSP+Caderno+PP_nº`) |
| `Codigo_evento` | ID do evento (`Ano+Mês+Dia+Base[4 letras]+nº`); repetido entre cidades do mesmo evento |
| `Data_de_Inicio_do_protesto` | Data de início do evento (ISO 8601; convertida de serial Excel) |
| `Cidade` | Cidade do registro |
| `Local` | Local específico (praça, via, assentamento etc.) |
| `Base_social`, `Base_social_2` | Categoria social que protesta (ver livro de código — 15 grupos) |
| `Alvo_protesto` | Alvo (Gov. Federal/Estadual/Municipal, Legislativo, Patronato, Sociedade etc.) |
| `Ocupação/Atividade` | Subclassificação de trabalhadores/atividade |
| `Objetivo_1`, `Objetivo_2` | Reivindicação/queixa (texto; codificável nas 11 categorias) |
| `Ambito_do_Protesto` | Local / Municipal / Estadual / Nacional |
| `Capilaridade`, `Unidade_Capilaridade` | Nº e tipo de unidades atingidas (vias, bairros, ocupações etc.) |
| `N_Part` | Número de participantes reportado |
| `Data_termino_do_protesto` | Data de término (ISO 8601; pode estar vazia) |
| `Org`, `Org_2`, `Org_3` | Organizações convocantes/apoiadoras |
| `Tipo_Protesto` | Repertório (Passeata/Marcha/Ato, Greve, Bloqueio, Ocupação, Panelaço etc.) |
| `Confronto_entre_manifestantes` | Sim / Não / NM |
| `Depredacao` | Sim / Não / NM |
| `Presenca_policia` | Sim / Não / NM |
| `Repressao_policial` | Sim / Não / NM |
| `Detidos`, `Feridos`, `Mortos` | Sim / Não / NM (NM = não mencionado) |

## Proveniência e integridade

- Os arquivos em `fonte-original/` são **cópias exatas** dos originais fornecidos, preservados para auditoria.
- O CSV em `dados/` é uma conversão **fiel** do XLSX. Única transformação aplicada: **datas seriais do Excel → ISO 8601** (base 1899-12-30, que corrige o bug do ano 1900 do Excel). Nenhum valor substantivo foi alterado, corrigido ou imputado.
- Eventuais inconsistências do banco original (ex.: divergências de estimativa de público entre notícias) são **preservadas tal como na fonte**, conforme a própria orientação do livro de código.

## Relação com o projeto

Este banco é **complementar** ao pipeline AEP próprio (`pipeline/`, Protocolo BEP-CEBRAP) e ao dataset `cycle_phases` (`data/cycle_phases.csv`). Enquanto o `cycle_phases` codifica **fases×ciclos** em escala ordinal, o banco NEPAC oferece **microdados evento-a-evento** para 2011–2016, permitindo:

- Validação empírica externa dos scores de EOP/DOS dos ciclos Junho 2013 e Impeachment Dilma.
- Análise de repertórios, alvos e bases sociais como evidência para as hipóteses H1–H3 (`docs/quadro-hipoteses.md`).
- Referência metodológica comparada: a definição de evento de Tatagiba & Galvão (Tilly 1978; Olzak 1989) dialoga diretamente com o Protocolo BEP-CEBRAP (Alonso et al. 2024) já adotado — ambas usam a Folha como fonte e o evento como unidade.

**Referência ABNT** (já incorporada em `artigo/referencias-abnt.md` — Tatagiba 2014, 2018; Tatagiba, Trindade & Teixeira 2015): a citação específica deste banco deve ser:

> TATAGIBA, Luciana; GALVÃO, Andreia. **Os protestos no Brasil em tempos de crise (2011-2016): banco de dados e livro de código.** Campinas: NEPAC/CEMARX, UNICAMP, 2019. Disponível em: https://nepac.ifch.unicamp.br/banco-de-dados.
