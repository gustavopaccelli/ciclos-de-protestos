# Cronologia Validada dos Ciclos de Protesto

**Última atualização:** 2026-07-03
**Objetivo:** Substituir referências de baixo prestígio (Terra.com.br, Politize.com.br, Wikipédia) por fontes jornalísticas e institucionais de alta confiabilidade para as datas-chave de cada ciclo.

**Fontes prioritárias utilizadas:**
- Agência Brasil / EBC (agenciabrasil.ebc.com.br)
- Portal da Câmara dos Deputados (camara.leg.br)
- Portal do Senado Federal (senado.leg.br)
- CPDOC/FGV (cpdoc.fgv.br)
- Fundação Perseu Abramo (fpabramo.org.br)

> **Nota metodológica sobre estimativas de público:** Em todos os ciclos existe divergência sistemática entre estimativas das Polícias Militares (maiores) e do Datafolha (menores, baseadas em contagem por amostragem fotográfica). A diferença pode alcançar até 5× (ex.: 15/mar/2015 em SP: PM = 1 mi; Datafolha = 210 mil). O banco `protest_events` deve registrar o valor reportado pela fonte (`crowd_size_reported`) e indicar a origem no campo `notes`.

---

## Ciclo 1 — Diretas Já (1983–1985)

| Data | Evento | Público estimado | Fonte confirmadora | Observações |
|---|---|---|---|---|
| **15 jun. 1983** | Comício inaugural — Praça Universitária, Goiânia | 5–15 mil | Jornal Opção (GO); Memorial da Democracia | Primeiro grande comício da campanha em Goiás. Não confundir com o comício de abril/1984. |
| **27 jul. 1983** | Comício de São Paulo (Estádio de Vila Euclides, Santo André) | ~10 mil | Agência Brasil (EBC) | Início simbólico da campanha no ABC paulista. |
| **25 jan. 1984** | Comício da Praça da Sé, São Paulo | **300 mil** | Agência Brasil (EBC); Rádio Câmara/Portal da Câmara dos Deputados | Data e público convergentes entre fontes. TV Globo na época enquadrou como "comemorações do aniversário de SP" (430 anos), evitando mencionar a pauta política. Acervo Folha confirma "300 mil" (retrospectivas). |
| **10 abr. 1984** | Comício da Candelária, Rio de Janeiro | **~1 milhão** | Agência Brasil (EBC); Jornal do Brasil; Rio Memórias | Maior manifestação política da história brasileira até aquela data. Data confirmada: 10 de abril. |
| **12 abr. 1984** | Comício da Praça Cívica, Goiânia | **~300 mil** | Agência Brasil Central (ABC/Goiás); Jornal Opção; Memorial da Democracia | ⚠️ **DISCREPÂNCIA CORRIGIDA**: fontes bootstrap indicavam "fevereiro de 1984" — confirmado como **12 de abril de 1984**. Não há registro de comício expressivo em Goiânia em fevereiro de 1984. |
| **16 abr. 1984** | Comício do Vale do Anhangabaú, São Paulo | **1,5 milhão** (estimativa majoritária); variações entre 400 mil e 1,5 mi | Agência Brasil (EBC); Fundação Perseu Abramo | Último e maior comício da campanha. Discrepância nas estimativas: fontes oficiais e a maioria citam 1,5 mi; análises mais críticas apontam 400 mil a 1 mi como capacidade real do espaço. |
| **25 abr. 1984** | Votação da Emenda Dante de Oliveira na Câmara | — | Portal da Câmara dos Deputados; Agência Brasil (EBC) | **Placar: 298 favoráveis × 65 contrários × 3 abstenções × 113 ausências.** Necessitava de 320 (2/3 do total). Derrota por apenas 22 votos. A emenda não foi ao Senado. |
| **15 jan. 1985** | Eleição de Tancredo Neves no Colégio Eleitoral | — | Portal da Câmara; Agência Brasil | Desfecho indireto do ciclo: a pressão das Diretas abriu brecha para a vitória oposicionista no Colégio Eleitoral. |

**Correção em `data/cycle_phases.csv`:** DJ-3 (pico) cobre 1984-04-01 a 1984-04-30 — compatível. Não há fase com "fevereiro/1984" como data de evento-chave; a menção ao comício de Goiânia em fase de expansão (DJ-2, jan–mar/1984) deve ser removida ou corrigida para indicar que o comício de Goiânia ocorreu no início da fase de pico (abr/1984).

---

## Ciclo 2 — Fora Collor / Caras-Pintadas (1992)

| Data | Evento | Público estimado | Fonte confirmadora | Observações |
|---|---|---|---|---|
| **11 ago. 1992** | 1.º grande ato dos caras-pintadas (MASP, São Paulo) | ~10 mil | Agência Brasil (EBC); CPDOC/FGV | Marco inicial do ciclo. Estudantes pintaram rostos com as cores do Brasil em protesto pelo afastamento de Collor. |
| **16 ago. 1992** | "Domingo Negro" — manifestação nacional de luto | Dezenas de milhares em múltiplas capitais | Ensinar História; Toda Matéria | Jovens vestiram preto e pintaram rostos de preto como sinal de luto. Data icônica que deu nome ao movimento. |
| **25 ago. 1992** | Pico em São Paulo | **~200 mil** | CPDOC/FGV | Maior concentração antes da votação na Câmara. |
| **29 set. 1992** | Votação do impeachment na Câmara dos Deputados | — | Portal da Câmara dos Deputados | **Placar: 441 favoráveis × 38 contrários × 1 abstenção × 23 ausências.** Mínimo necessário: 336 (2/3). Sessão durou 9h18min. |
| **29 dez. 1992** | Renúncia de Collor (carta lida no início da sessão do Senado) | — | CNN Brasil; Portal da Câmara; Agência Brasil | Collor renunciou antes de ser julgado. |
| **30 dez. 1992** | Condenação formal pelo Senado (mesmo após renúncia) | — | Senado Federal; Agência Brasil | **Placar: 76 × 2** pela inabilitação política por 8 anos. O processo prosseguiu após a renúncia e resultou em condenação no dia seguinte. |

---

## Ciclo 3 — Junho de 2013

| Data | Evento | Público estimado | Fonte confirmadora | Observações |
|---|---|---|---|---|
| **6 jun. 2013** | 1.º ato — bloqueio espontâneo (Estrada do M'Boi Mirim, SP) | Pequeno | Agência Brasil (EBC) | Ato espontâneo, sem convocação formal do MPL. |
| **7 jun. 2013** | 1.º ato formalmente convocado pelo MPL (Largo da Batata, SP) | ~2 mil | Agência Brasil (EBC); Artigo 19 | Primeiro ato com convocação oficial. Diversas fontes usam 6/6 como marco inicial do ciclo; o protocolo BEP adota a primeira ação confirmada (6/6). |
| **13 jun. 2013** | 4.º ato — repressão policial ao MPL | — | Artigo 19 (relatório); Agência Brasil | **232 detidos; mais de 100 feridos** (incluindo 17 jornalistas). Fotógrafo Sérgio Silva perdeu a visão do olho esquerdo. Após a repressão, Folha, Estadão e Globo — que até então criticavam os manifestantes — passaram a criticar a violência policial. Virada editorial: 13–17 de junho. |
| **17 jun. 2013** | 5.º ato — 1.ª onda nacional de protestos | Dezenas de milhares em SP e outras capitais | Rio Memórias; Agência Brasil | Manifestações se expandem para além de SP. Pautas extrapolam a tarifa de ônibus. |
| **20 jun. 2013** | Pico máximo das manifestações | **~1,2 milhão** no Rio de Janeiro (Av. Pres. Vargas); estimativas nacionais: 1–1,5 mi | Rio Memórias; Agência Brasil | Maior manifestação da história do Rio até aquela data. Estimativas nacionais somam entre 1 mi e 1,5 mi em todo o país. |

---

## Ciclo 4 — Impeachment de Dilma Rousseff (2014–2016)

| Data | Evento | Público estimado | Fonte confirmadora | Observações |
|---|---|---|---|---|
| **26 out. 2014** | Reeleição de Dilma Rousseff | — | TSE; Agência Brasil | Marco inicial do ciclo de oposição (data adotada em `cycle_phases.csv`: ID-1 emergencia = 2014-10-26). |
| **15 mar. 2015** | 1.ª grande manifestação nacional | **PM-SP: 1 mi** em SP; **Datafolha: 210 mil** em SP; **total nacional (PM): ~1,9 mi** | Datafolha (citado em CESOP/Unicamp); Agência Brasil | Manifestações em 212 cidades. Datafolha classificou como a maior manifestação em SP desde as Diretas Já. Discrepância PM × Datafolha: ver nota metodológica acima. |
| **16 ago. 2015** | 2.ª grande manifestação nacional | **PM: 879 mil a 2 mi** (total); **Datafolha: 135 mil** em SP | Agência Brasil; Jovem Pan | Em 291 cidades. Convocada por MBL, Vem pra Rua e Revoltados Online. Mesma divergência metodológica PM × Datafolha. |
| **13 mar. 2016** | Maior manifestação da série e da história política do Brasil | **PM (nacional): 3,6 mi**; **organizadores: 6,9 mi** | Agência Brasil; Portal da Câmara | Superou o comício da Candelária (1984) em público estimado pela PM. Ocorreu em todos os estados e no DF. |
| **17 abr. 2016** | Votação do impeachment na Câmara dos Deputados | — | Portal da Câmara dos Deputados | **Placar: 367 favoráveis × 137 contrários × 7 abstenções.** Necessário: 342 (2/3). Aprovado. O voto 342 foi do deputado Bruno Araújo (PSDB-PE) às 23h08. |
| **11–12 mai. 2016** | Votação no Senado — abertura do processo e afastamento provisório de Dilma | — | Senado Federal; Agência Brasil | **Placar: 55 × 22** (2 ausências). Sessão durou ~20 horas. Dilma foi afastada por até 180 dias. |
| **31 ago. 2016** | Votação final no Senado — impeachment consumado | — | Senado Federal; CNN Brasil | **Placar: 61 × 20** pela perda do mandato. Em segunda votação (inabilitação política), 42 × 36 — não atingiu os 54 necessários; Dilma manteve os direitos políticos. |

---

## Resumo das Discrepâncias Corrigidas

| Ciclo | Item | Dado anterior (bootstrap) | Dado corrigido | Impacto em `cycle_phases.csv` |
|---|---|---|---|---|
| Diretas Já | Comício de Goiânia | "fevereiro de 1984" | **12 de abril de 1984** | Nenhum (fase DJ-2 cobre jan–mar; o comício pertence à fase DJ-3 abr/1984 — já correto) |
| Fora Collor | Renúncia de Collor e encerramento do processo | 29/dez confundido com fim do processo | Renúncia = 29/dez/1992; condenação Senado = 30/dez/1992 (76×2) | Fase FC-5 (desfecho = 1992-12-29 a 1992-12-31) — compatível |
| Impeach. Dilma | Público 15/mar/2015 | "1–3 milhões" (genérico) | PM-SP: 1 mi; Datafolha: 210 mil; PM nacional: 1,9 mi | Fase ID-2 (expansao) — não altera scores |
| Impeach. Dilma | Público 13/mar/2016 | "5,6–6,9 milhões" | PM nacional: 3,6 mi; organizadores: 6,9 mi | Fase ID-3 (pico) — não altera scores |

## Fontes consultadas

- [Comício símbolo das Diretas Já completa 40 anos — Agência Brasil](https://agenciabrasil.ebc.com.br/geral/noticia/2024-01/comicio-simbolo-das-diretas-ja-completa-40-anos)
- [Rádio Câmara — 25 jan. 1984, 300 mil na Praça da Sé](https://www.camara.leg.br/radio/programas/279710)
- [Comício da Candelária 40 anos — Agência Brasil](https://agenciabrasil.ebc.com.br/politica/noticia/2024-04/comicio-da-candelaria-40-anos-o-legado-sociopolitico-das-diretas-ja)
- [Comício do Anhangabaú 40 anos — Agência Brasil](https://agenciabrasil.ebc.com.br/politica/noticia/2024-04/comicio-das-diretas-ja-no-anhangabau-em-sao-paulo-completa-40-anos)
- [16/04/1984: Vale do Anhangabaú — Fundação Perseu Abramo](https://fpabramo.org.br/2020/04/16/6-05-84-vale-do-anhangabau-virou-mar-de-gente/)
- [Votação Emenda Dante de Oliveira — Agência Brasil](https://agenciabrasil.ebc.com.br/politica/noticia/2024-04/votacao-de-emenda-que-pedia-eleicoes-diretas-completa-40-anos)
- [Emenda Dante de Oliveira — Portal da Câmara dos Deputados](https://www.camara.leg.br/radio/programas/431737)
- [Comício de Goiânia — Jornal Opção](https://www.jornalopcao.com.br/colunas-e-blogs/periscopio/o-comicio-das-diretas-em-goiania-648662/)
- [Caras-Pintadas — CPDOC/FGV](https://www18.fgv.br/cpdoc/acervo/dicionarios/verbete-tematico/caras-pintadas)
- [Votação impeachment Collor — Portal da Câmara](https://www2.camara.leg.br/agencia/noticias/POLITICA/427000)
- [Collor renúncia — CNN Brasil](https://www.cnnbrasil.com.br/politica/collor-renunciou-para-escapar-da-inelegibilidade-em-1992)
- [Câmara autoriza impeachment Dilma — Portal da Câmara](https://www2.camara.leg.br/camaranoticias/noticias/POLITICA/507325)
- [Senado — votações no impeachment Dilma](https://www12.senado.leg.br/noticias/materias/2016/12/28/veja-como-votaram-os-senadores-no-julgamento-de-dilma-rousseff)
