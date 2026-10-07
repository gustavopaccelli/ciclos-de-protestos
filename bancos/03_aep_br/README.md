# AEP-BR: banco próprio de eventos de protesto (1983–hoje)

Este é o banco de eventos de protesto construído pelo projeto a partir da imprensa nacional e de diários oficiais. Ele segue o protocolo do BEP (Alonso et al. 2024, *Plural* 31(2)).

| Pasta | Conteúdo |
|---|---|
| [`codebook/`](codebook/) | `codebook_aep_br.md` (para leitura) e `codebook_aep_br.yaml` (especificação para o pipeline), versão 1.0 |
| [`fontes/`](fontes/) | `fontes_aep_br.csv`, com veículos, períodos, tipo de acesso e prioridade |
| [`sementes/`](sementes/) | eventos codificados à mão: 59 de Diretas Já (1983–84) e 15 de Fora Collor (1992) |
| [`coleta/`](coleta/) | saída do scraper do Acervo Folha (`acervo_protestos.json`, `folha_acervo/`) e `metadata_folha.json` |

O banco SQLite gerado pelo pipeline (`protest_events.db`) fica nesta pasta e é ignorado pelo git.

## Estado atual

- O codebook está na versão 1.0. As decisões estão no §6 do `codebook_aep_br.md`.
- A coleta não começou:
  - O scraper da Folha precisa de credenciais de assinante, definidas em `.env` na raiz a partir de `.env.example`.
  - O workflow diário do GitHub Actions foi **desativado em 2026-10-07** depois de falhar em todas as execuções desde 27/09. Ainda é possível rodá-lo à mão, pela aba Actions, com `workflow_dispatch`.
- O `config/doca_codebook.yaml` continua sendo o que o codificador (`src/preprocessing/coder.py`) lê. A migração do codificador para o esquema AEP-BR é o próximo passo.

## Próximos passos

1. Adaptar `src/preprocessing/coder.py` e `src/data/init_doca_database.py` ao `codebook_aep_br.yaml`.
2. Fazer um piloto em 2013 com a Folha e validar contra o NEPAC.
3. Expandir para 1983–1992, onde as sementes servem de gold standard, e depois para 2017 em diante.
