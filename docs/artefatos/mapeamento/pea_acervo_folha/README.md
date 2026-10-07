# PEA — Acervo Folha de S.Paulo

Pipeline automatizado de **Análise de Eventos de Protesto** (PEA/AEP)
baseado no protocolo DoCA (*Dynamics of Collective Action*).

Coleta artigos do Acervo Folha, identifica e codifica eventos de protesto
usando a API Claude (Anthropic), e consolida um dataset estruturado.

---

## Estrutura do projeto

```
pea_acervo_folha/
├── .env.example            ← Modelo de configuração (copiar para .env)
├── requirements.txt
├── run_pipeline.py         ← Ponto de entrada principal
│
├── config/
│   ├── queries.yaml        ← Termos de busca e filtros de seção
│   └── doca_codebook.yaml  ← Claim codes, repertórios, escalas
│
├── scripts/
│   ├── 01_scraper.py       ← Coleta via Playwright (browser headless)
│   ├── 02_doca_coder.py    ← Codificação via Claude API
│   ├── 03_build_dataset.py ← Consolidação e exportação CSV/XLSX
│   └── 04_intercoder_reliability.py  ← Cohen's Kappa
│
├── docs/
│   └── TUTORIAL.md         ← Tutorial completo passo a passo
│
└── output/                 ← Criado automaticamente
    ├── raw_articles/
    ├── coded_events/
    ├── rejected_articles/
    ├── human_coded/
    ├── logs/
    └── dataset/
```

---

## Início rápido

```bash
# 1. Configure o ambiente
cp .env.example .env
# edite .env com suas credenciais

# 2. Instale dependências
pip install -r requirements.txt
python -m playwright install chromium

# 3. Execute o pipeline
python run_pipeline.py --step all
```

Consulte `docs/TUTORIAL.md` para instruções detalhadas.

---

## Referências

- BEP-Cebrap (NIPOMS/USP) — Angela Alonso et al.
- NEPAC/Unicamp — Luciana Tatagiba & Andréia Galvão
- DoCA Project — McAdam, Tarrow & Tilly
