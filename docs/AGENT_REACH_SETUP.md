# Agent Reach Setup & Configuration

**Instalação concluída em**: 2026-09-20  
**Versão**: Agent Reach v1.5.0  
**Ambiente**: Python 3.11.15

---

## 📦 Status da Instalação

✅ **Instalado com sucesso** em `~/.agent-reach-venv/`

### Dependências Instaladas
- agent-reach v1.5.0
- yt-dlp (para YouTube)
- feedparser (para RSS/Atom)
- requests (para web scraping)
- rich (interface visual)
- E mais 15+ dependências de suporte

---

## 🚀 Como Usar Agent Reach

### Opção 1: Via Script Local (Recomendado)
```bash
cd /home/user/research
./agent-reach.sh --help
./agent-reach.sh install --env=auto
./agent-reach.sh doctor
```

### Opção 2: Ativar venv e usar diretamente
```bash
source ~/.agent-reach-venv/bin/activate
agent-reach --help
agent-reach install --env=auto --system
agent-reach doctor
```

### Opção 3: Criar alias (opcional)
Adicione ao seu `~/.bashrc` ou `~/.zshrc`:
```bash
alias agent-reach='source ~/.agent-reach-venv/bin/activate && agent-reach'
```

---

## 📊 Status Atual dos Canais

### ✅ Canais Ativos (2/16)
- **RSS/Atom Feeds** — Leitura de RSS/Atom feeds
- **Qualquer Página Web** — Via Jina Reader (curl https://r.jina.ai/URL)

### ⚠️ Canais com Dependências Faltantes
- **GitHub** — Requer GitHub CLI (`gh`)
- **YouTube** — yt-dlp instalado, mas JS runtime não configurado
- **V2EX** — Conectividade de rede/proxy necessária

### ❌ Canais Desabilitados (14/16)
Disponíveis para instalação:
- Twitter/X (tweets)
- Reddit (posts e comments)
- Facebook (posts, pages, groups)
- Instagram (users, feed, posts)
- Bilibili (videos, subtitles, search)
- Xiaohongshu (小红书 notes)
- Ximalaya (小宇宙 podcasts)
- Snowball (雪球 stocks/community)
- LinkedIn (professional)
- Boss (Boss直聘 job listings)
- E mais...

---

## 🔧 Comandos Úteis

### Verificar Status Completo
```bash
./agent-reach.sh doctor
```

### Instalar Canais Específicos
```bash
./agent-reach.sh install --env=auto --system --channels=github,youtube,twitter
```

### Instalar Todos os Canais (requer configuração)
```bash
./agent-reach.sh install --env=auto --system --channels=all
```

### Ver Configurações Salvas
```bash
./agent-reach.sh configure list
```

### Configurar Proxy (se necessário)
```bash
./agent-reach.sh configure proxy
```

---

## 📋 Próximos Passos Recomendados

### 1. Instalar GitHub CLI (Prioridade Alta)
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

Então habilitar GitHub:
```bash
./agent-reach.sh install --env=auto --system --channels=github
```

### 2. Configurar YouTube (se necessário)
```bash
mkdir -p /root/.config/yt-dlp
echo '--js-runtimes node' >> /root/.config/yt-dlp/config
```

### 3. Configurar MCP (Semantic Search)
```bash
npm install -g mcporter
mcporter config add exa https://mcp.exa.ai/mcp --scope home
```

### 4. Configurar Proxy (China Mainland)
Se usar VPN/proxy em China Mainland:
```bash
./agent-reach.sh configure proxy
```

---

## 🔐 Segurança & Boas Práticas

⚠️ **IMPORTANTES**:

1. **Use contas secundárias** para plataformas que requerem autenticação
2. **Nunca use contas primárias/principais** com Agent Reach
3. **Use Cookie-Editor** para plataformas como Twitter/X, Xiaohongshu
4. **Nunca compartilhe** cookies ou credenciais
5. **Ative proxy** se em China Mainland (muitas plataformas têm firewalls)

### Credenciais Seguras
Para plataformas que requerem login:
- GitHub: Use Personal Access Token (PAT) com scopes mínimos
- Twitter/X: Use Cookie-Editor + conta secundária
- Reddit: Use Reddit account + rdt-cli
- Xiaohongshu: Use Cookie-Editor + conta secundária

---

## 📚 Documentação

- **Repositório**: https://github.com/Panniantong/agent-reach
- **Documentação Oficial**: https://github.com/Panniantong/agent-reach/tree/main/docs
- **Issues & Feedback**: https://github.com/Panniantong/agent-reach/issues

---

## 🔍 Troubleshooting

### "agent-reach: command not found"
Solução: Use o script local `./agent-reach.sh` ou ative a venv:
```bash
source ~/.agent-reach-venv/bin/activate
```

### "mcporter not installed"
Não é crítico. Instale apenas se precisar de semantic search:
```bash
npm install -g mcporter
```

### "GitHub CLI not found"
Instale conforme seu SO:
```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

### Erro de conectividade (V2EX, China Mainland)
Se em China Mainland, configure proxy:
```bash
./agent-reach.sh configure proxy
```

---

## 📝 Arquivos Relacionados

- **Script de execução**: `./agent-reach.sh`
- **Este documento**: `docs/AGENT_REACH_SETUP.md`
- **Venv**: `~/.agent-reach-venv/`
- **Configuração**: `~/.agent-reach/` (será criado após primeiro uso)

---

**Última atualização**: 2026-09-20  
**Status**: ✅ Operacional
