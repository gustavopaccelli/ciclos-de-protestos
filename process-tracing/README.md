# Levantamento por process tracing em fontes oficiais

Mapeamento dos quatro ciclos de protesto em **fontes oficiais do Estado brasileiro**,
organizado em três tempos: antecedente (T-1), ciclo (T0) e desfechos (T+1).

É a quarta perna da base probatória do projeto — e a única independente da imprensa. A AEP
do projeto e o banco NEPAC apoiam-se ambos na Folha; só a Mass Mobilization era
genuinamente externa, e com N pequeno.

**Estado atual:** infraestrutura completa, varredura não iniciada. O registro contém 8
evidências-semente (4 verificadas, 3 pendentes, 1 com divergência aberta em fonte oficial).

---

## Como se articula com o resto do repositório

| Já existe | O que faz | Este levantamento |
|---|---|---|
| `pipeline/` + `docs/aep-protocol-bep.md` | AEP no Acervo Folha, nível do evento | não duplica; usa o AEP como T0 |
| `docs/cronologia-validada.md` | datas-chave validadas | referencia, não reescreve |
| `experiments/` | memorandos exploratórios de 2026-06 | herda a prática de predições registradas |
| `data/cycle_phases.csv` | escores ordinais por fase | fornece FK; não altera |
| `artefatos/tese/` | tese de Costa (2024) | eleva sua base de secundária para primária |

## Ancoragem na tese

Os vocabulários deste levantamento não vêm de um esquema genérico de process tracing.
Cada um deriva do arcabouço já mobilizado na tese, com a localização no texto registrada
em `codebook-evidencia.yaml`:

- **Dimensões do T-1 conjuntural** — as quatro categorias de análise de conjuntura de
  Herbert José de Souza (1986) que a tese adota na METODOLOGIA.
- **Mecanismos** — emergência, difusão, repressão, radicalização (Tilly & Tarrow; McAdam
  et al.), mais polarização, inovação e coalescência, nomeados nas Considerações Finais.
- **Indicadores estruturais** — o Quadro 3 da tese (Chenoweth & Ulfelder, 2015), que a tese
  adota como heurística mas **nunca mede para o Brasil**. Aqui ele é operacionalizado com
  equivalentes oficiais brasileiros: é a contribuição empírica mais original desta pasta.
- **Quadro 8 ampliado** — o quadro comparativo das Considerações Finais, estendido do
  terceiro ao quarto ciclo e com exigência de âncora documental por célula.

Três achados da releitura da tese moldaram o desenho: ela é declaradamente baseada em
fontes secundárias; as Diretas Já a sustentam teoricamente sem terem sido tratadas
empiricamente; e o Quadro 8 já era o embrião deste trabalho. Detalhes no `PROTOCOLO.md` §2.

## Estrutura

```
PROTOCOLO.md              desenho, camadas do T-1, testes de Van Evera, riscos
codebook-evidencia.yaml   vocabulários controlados, cada um com fonte na tese
fontes/                   hierarquia de 4 níveis e caminho de busca por repositório
ciclos/c*/dossie.md       dossiê narrativo por ciclo, T-1e / T-1c / T0 / T+1
dados/
  registro_evidencias.csv   tabela central, uma linha por peça de evidência
  marcos_institucionais.csv atos oficiais datados; encadeia ciclos via ciclo_seguinte_afetado
  series_estruturais.csv    bateria Chenoweth & Ulfelder, 1970-2016
  quadro8_ampliado.csv      36 células (9 categorias x 4 ciclos)
scripts/                  extratores das APIs oficiais + validador
```

## Uso

```bash
# validação completa — roda offline, sem dependência de rede
python process-tracing/scripts/valida_registro.py

# extração (exige máquina com acesso à internet)
python process-tracing/scripts/extrai_camara_senado.py --ciclo c2 --dry-run
python process-tracing/scripts/extrai_series_estruturais.py --listar
python process-tracing/scripts/extrai_series_estruturais.py --indicador inflacao
```

Dependências: `pandas`, `pyyaml` (já em `pipeline/requirements.txt`). Os extratores usam
só a biblioteca padrão.

## Limitações declaradas

**Os extratores não foram testados contra as APIs.** O ambiente em que foram escritos
bloqueia todo egresso de rede (403 no CONNECT). A estrutura das requisições segue a
documentação pública de cada API, mas a primeira execução com rede deve começar por
`--dry-run` e conferir o retorno antes de gravar qualquer coisa.

**Cobertura histórica desigual.** As APIs cobrem bem o período recente. Para 1983–1992
(C1 e C2) a fonte de nível 1 são os Diários da Câmara e do Congresso digitalizados, que
**não têm API** — a recuperação é manual, pelo caminho documentado em
`fontes/registro-fontes.md`, que já traz as páginas exatas de três sessões-chave.

**Nada entra por memória.** Toda linha marcada como verificada carrega `fonte_url` e
`data_consulta`, e o validador recusa o contrário. O que não foi recuperado fica
`pendente`, com o caminho de busca anotado.

## Próximo passo

Antes de qualquer varredura: **registrar as predições** de cada ciclo no dossiê
correspondente, com data (PROTOCOLO §5). Enquanto a seção de predições estiver vazia, a
evidência coletada é exploratória e não serve para testar hipótese.
