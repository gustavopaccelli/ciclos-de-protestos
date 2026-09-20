# Dados complementares — Diretas Já (1983–1984)

Dados incorporados em 2026-07-14 a partir dos arquivos enviados pelo pesquisador
(`artefatos/Cronologia_Diretas_Ja.xlsx` e `artefatos/Manifestacoes_e_Dados_Diretas_Ja.xlsx`).
Complementam a codificação da campanha das Diretas Já.

## Arquivos

| Arquivo | Conteúdo | Origem |
|---|---|---|
| `comicios_cronologia.csv` | 50 comícios com data, cidade/UF e público estimado (nov/1983 a jun/1984) | aba "Cronologia Comícios" |
| `comicios_por_estado.csv` | Distribuição dos comícios por estado (N e %); **total Brasil: 490 comícios** | aba "Roteiro por Estado" |
| `grupos_associacoes.csv` | Categorias de atores da campanha (sindicatos, associações profissionais, estudantis, partidos, mídia, movimentos sociais) | aba "Grupos e Associações" |

Fontes das planilhas: Folha de S.Paulo, O Estado de S.Paulo, Veja, IstoÉ, Senhor,
Kotscho (1984), Rodrigues (2003), Leonelli & Oliveira (2004), Bertoncelo (2007).

## Relação com os demais dados

- **Não duplicar com** `data/protest_events_seeds/protest_events_diretas_ja_seed.csv`: a aba
  "Manifestações por Mês" do arquivo original **sobrepõe-se** ao seed (mesmos eventos,
  mesmas fontes por estimativa) e por isso **não** foi reconvertida — o seed permanece a
  versão canônica no nível do evento, com mín/máx/mediana por fonte.
- Estes arquivos acrescentam o que o seed não tinha: a **distribuição estadual agregada**
  (roteiro nacional dos 490 comícios) e a **tabela de atores/associações** da coalizão.

## Achados de interesse

- **Concentração regional:** São Paulo (170 comícios, 34,7%) e Minas Gerais (85, 17,3%)
  respondem por mais da metade dos 490 comícios — evidência da geografia da mobilização.
- **Coalizão suprapartidária ampla:** CUT/CONCLAT, OAB, ABI, SBPC, UNE/UBES, CEBs, movimentos
  feminista/negro/ecológico e os partidos PMDB, PT, PDT, PTB (+ dissidência pró-Diretas do
  PDS) — sustenta a codificação alta de `op_aliados_influentes` na fase de pico.
- **Estimativas de público** (comícios-chave): Sé/SP 25/01 (200–250 mil); Candelária/RJ 10/04
  (~1 milhão); Goiânia 12/04 (200–250 mil, reforça a correção da data para abril);
  Anhangabaú/SP 16/04 (1,5 milhão). Divergências entre fontes preservadas.
