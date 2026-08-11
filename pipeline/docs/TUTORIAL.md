# Tutorial — Pipeline PEA (Acervo Folha → protest_events)

## 1. Instalação (uma vez)

```bash
cd pipeline
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env   # e preencha FOLHA_EMAIL, FOLHA_PASSWORD, ANTHROPIC_API_KEY
```

## 2. Validação dos seletores (FAÇA ISTO PRIMEIRO)

Os seletores CSS do Acervo **nunca foram validados contra o site logado** e a
aplicação é React: eles mudam. Sem esta etapa a coleta retorna zero.

```bash
cd pipeline
python 01_scraper.py --diagnose --headed
```

O navegador abre visível, faz login, executa **uma** busca e grava em
`pipeline/data/diagnose/`: HTML e screenshot das páginas de login, busca e
artigo, mais um `relatorio.txt` dizendo **quantos elementos cada seletor
encontrou**. Seletor com `0 elemento(s)` está errado.

Para consertar, edite **`pipeline/config/selectors.yaml`** — não é preciso
mexer em Python. Cada chave aceita uma *lista de candidatos*, tentados em
ordem; no navegador use `F12 → Elements`, botão direito no elemento certo →
`Copy → Copy selector`, e cole como primeiro item. Repita o `--diagnose` até
todos os grupos acusarem mais de zero.

## 3. Coleta (retomável; horas a dias)

```bash
python 01_scraper.py --dry-run          # lista o que coletaria, sem baixar
python 01_scraper.py --limit 20         # teste barato: 20 artigos
python run_pipeline.py --step scrape    # coleta completa
```

- O estado fica em `pipeline/data/scrape_state.json`; interrompa e retome à
  vontade. O progresso é gravado **a cada página** de resultados.
- Artigos brutos: `pipeline/data/raw/*.json` (1 arquivo por matéria).
- O script **aborta com mensagem** se o login não se confirmar, em vez de
  coletar zero silenciosamente.

## 4. Codificação DoCA (controle de custo por lote)

```bash
python run_pipeline.py --step code --batch 100
```

- Modelo padrão: `claude-opus-4-8` (defina `DOCA_MODEL=claude-sonnet-4-6` no
  `.env` para triagem mais barata; recodifique casos difíceis com Opus depois).
- O system prompt (instruções DoCA + codebook) usa **prompt caching** — a
  partir do 2º artigo o custo de entrada cai ~90%.
- A saída usa **structured outputs** (JSON schema): todo evento sai validado
  contra o codebook (claim_code, repertório e escala de multidão são enums).
- Estimativa de custo (Opus 4.8, matéria média ~1.500 tokens): ~US$ 0,01–0,03
  por artigo com cache; um corpus de 10 mil matérias ≈ US$ 100–300.
  Com Sonnet 4.6, ~1/2 disso.
- Incremental: artigos já codificados (`pipeline/data/coded/`) são pulados.

## 5. Dataset final

```bash
python run_pipeline.py --step build
```

Gera três saídas:
- `data/protest_events_raw.csv` — **uma linha por extração**, sem deduplicação
  (registro auditável: quantas fontes cobriram cada evento);
- `data/protest_events.csv` — uma linha por **evento canônico**;
- `data/protest_events.xlsx` — 4 abas: eventos, agregação anual, frequência de
  claims, distribuição geográfica.

Durante a execução o script avisa sobre valores fora do codebook e variáveis
com mais de 30% de ausência (protocolo §7).

## 6. Confiabilidade intercodificadores

1. Sorteie uma amostra **estratificada por ciclo** (≥10% do corpus ou 100
   artigos por ciclo, o que for maior — protocolo §12.3; amostra aleatória
   simples sub-representaria os ciclos pré-2011, os mais difíceis de codificar)
   e codifique manualmente num CSV com `event_id` + as variáveis a aferir.
   O script cobre 16 variáveis; inclua no CSV as que quiser medir.
2. Rode:

```bash
python 04_intercoder_reliability.py amostra_manual.csv --out kappa.csv
```

Reporte o Kappa por variável no paper. **Limiar do projeto: κ ≥ 0,75**
(Krippendorff 2004), conforme `config/doca_codebook.yaml` e
`docs/aep-protocol-bep.md` §8/§11. Variáveis abaixo do limiar exigem revisão do
prompt ou exclusão da análise — não são reportadas como válidas.

## 7. Exportação para R/Stata

```r
df <- read.csv("data/protest_events.csv")          # R
```
```stata
import delimited "data/protest_events.csv", clear  // Stata
```

## Avisos

- `config/doca_codebook.yaml` é uma **reconstrução** do codebook original
  (o YAML da sessão anterior não está no repositório). Valide os claim codes
  antes de codificar em escala.
- Respeite os termos de uso do Acervo Folha; a coleta usa sua assinatura
  pessoal com delay de 2s entre requisições.
- Nunca commite o `.env`.
