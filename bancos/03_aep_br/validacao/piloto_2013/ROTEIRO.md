# Roteiro do piloto 2013 (tarefas B6 e B11)

O piloto testa duas coisas ao mesmo tempo: se o pipeline completo funciona na Folha de 2013 e se as três variáveis experimentais do bloco X do codebook (`aliados_institucionais`, `reacoes_publicas`, `tom_cobertura`) podem ser codificadas com confiabilidade. Ele roda no seu computador, porque precisa do login de assinante da Folha.

Amostra: 100 matérias da janela `junho_2013` de `config/queries.yaml` (mai–dez/2013), estratificadas pela fase do ciclo em que foram publicadas, com um estrato para os meses fora do ciclo. A semente do sorteio é fixa.

Todos os comandos são rodados a partir da raiz do repositório.

## 1. Preparar (uma vez)

```bash
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env    # preencha FOLHA_EMAIL, FOLHA_PASSWORD e ANTHROPIC_API_KEY
python src/data/check_schema_coverage.py
```

O `.env` nunca vai para o git.

## 2. Validar os seletores do Acervo

```bash
python src/data/scraper.py --diagnose --headed
```

Confira o relatório em `bancos/03_aep_br/coleta/folha_acervo/diagnose/`. Seletor com 0 elementos está errado: corrija em `config/selectors.yaml` e repita até todos acharem algo. Confira também se a matéria salva traz seção e página: elas alimentam a medida de visibilidade (`teoria/matriz.yaml`, `dos_visibilidade`).

## 3. Coletar 2013

```bash
python src/data/scraper.py --janela junho_2013 --dry-run --limit 50   # confere a busca
python src/data/scraper.py --janela junho_2013
```

A coleta é retomável. As matérias ficam em `bancos/03_aep_br/coleta/folha_acervo/`, fora do git.

## 4. Sortear a amostra

```bash
python src/preprocessing/piloto.py amostra --n 100
```

Gera `amostra.csv` nesta pasta e mostra quantas matérias saíram de cada estrato.

## 5. Codificar com o LLM

Primeiro 20, para medir o custo (o uso de tokens fica gravado em cada JSON, em `_usage`):

```bash
python src/preprocessing/coder.py --amostra bancos/03_aep_br/validacao/piloto_2013/amostra.csv --batch 20
python src/preprocessing/coder.py --amostra bancos/03_aep_br/validacao/piloto_2013/amostra.csv
```

## 6. Gerar a planilha cega e codificar à mão

```bash
python src/preprocessing/piloto.py planilha
```

Gera `gold_standard.csv` com uma linha por evento que o LLM encontrou. Só as colunas de identificação vêm preenchidas (matéria, `evento_id`, data, cidade); as variáveis a aferir vêm vazias. **Não abra os JSON da codificação automática antes de terminar**, para a codificação manual ser independente.

Para cada matéria, leia o texto em `coleta/folha_acervo/` e preencha:

- **Núcleo do codebook:** as colunas de vocabulário fechado e as booleanas, pelo `codebook_aep_br.md`. Nas listas, use o valor principal (ou vários separados por `;`; só o primeiro é comparado).
- **Experimentais:**
  - `tom_cobertura`: `legitimadora`, `neutra`, `criminalizadora` ou `SI`, julgando o texto do jornal, não as falas citadas.
  - `aliado_presente` (`true`/`false`) e `aliado_tipo_principal` (`parlamentar`, `governante`, `judiciario_mp`, `partido`, `outro` ou `nenhum`).
  - `reacao_apoio` e `reacao_rejeicao` (`true`/`false`): a matéria registra reação de apoio, ou de rejeição, de alguém que não participa do ato.
- **Unitização:** se a linha não é um evento de protesto, marque `elegivel = false`. Se a matéria relata um evento que não está na planilha, acrescente uma linha com `evento_id` = `manual-<arquivo>-<n>`. Linhas com `evento_id` vazio são matérias em que o LLM não achou evento: preencha `evento_id` só se você achar um.

As definições completas estão no `codebook_aep_br.yaml` (vocabulários `aliado_tipo`, `reacao_sinal`, `tom_cobertura`) e no §7 do `codebook_aep_br.md`.

## 7. Calcular a confiabilidade

```bash
python src/analysis/run_pipeline.py --step kappa --manual bancos/03_aep_br/validacao/piloto_2013/gold_standard.csv
```

O relatório sai em `bancos/03_aep_br/validacao/kappa_<data>.csv`, separado em `nucleo` e `experimental`, com a contagem de eventos que só um dos lados encontrou.

## 8. Decidir (B11)

Uma variável experimental entra no codebook se atingir κ ≥ 0,75 (limiar do projeto). Abaixo disso, há duas saídas: revisar a regra no prompt e testar de novo, ou descartar. Registre a decisão no `research-log.md` e atualize o status do conceito em `teoria/matriz.yaml`. Versione `amostra.csv`, `gold_standard.csv` e o relatório de kappa; as matérias brutas continuam fora do git.

Se o kappa do núcleo também ficar abaixo do limiar, o problema é do codebook ou do prompt como um todo, não das experimentais: resolva isso antes de expandir a coleta.
