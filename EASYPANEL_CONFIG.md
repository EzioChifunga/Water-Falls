# 🎯 Configuração Final para EasyPanel Hostinger

Resumo rápido das configurações que você precisa colocar no EasyPanel.

---

## 📋 Dockerfile (COPIE EXATAMENTE ISTO)

```dockerfile
# ====================================
# WaterFalls API - Dockerfile EasyPanel
# Otimizado para Hostinger com EasyPanel
# ====================================

# Stage 1: Build
FROM python:3.13-slim as builder

WORKDIR /tmp/build

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requirements
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (Imagem final menor)
FROM python:3.13-slim

WORKDIR /app

# Instalar apenas ferramentas de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar pacotes Python instalados do builder
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY . .

# Configurar variáveis de ambiente
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Criar diretórios necessários
RUN mkdir -p /app/logs

# Health check para EasyPanel
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Expor porta (EasyPanel vai mapear)
EXPOSE 8000

# Comando de inicialização
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 🔑 Environment Variables (Variáveis de Ambiente)

Adicione no EasyPanel em **Variáveis de Ambiente**:

```
DATABASE_URL=postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

---

## ⚙️ Configurações EasyPanel

### Nome da Aplicação:
```
WaterFalls API
```

### Tipo:
```
Docker
```

### Repositório GitHub:
```
seu-usuario/WaterFalls-API
Branch: master
```

### Dockerfile Path:
```
./Dockerfile
```

### Porta Interna:
```
8000
```

### Porta Externa:
```
8000 (ou deixar EasyPanel escolher automaticamente)
```

---

## 📁 Volumes (Opcional)

Se quiser persistir dados:

```
Container Path: /app/migrations
Host Path: /data/migrations

Container Path: /app/logs
Host Path: /data/logs
```

---

## 🌐 Domínio

Se tiver domínio:

```
Domínio: seu-dominio.com
SSL: Ative (automático com Let's Encrypt)
```

---

## ✅ Depois de Criar

### 1. Aguardar Build
- Tempo: ~5-10 minutos
- EasyPanel vai clonar repo, construir imagem e iniciar

### 2. Verificar Health Check
- EasyPanel testa automaticamente
- Status deve ser ✅ Green

### 3. Rodar Migrations (Primeira Vez)
Via SSH ou Console EasyPanel:
```bash
docker exec waterfalls-api alembic upgrade head
```

### 4. Acessar API
```
http://seu_ip_vps:8000/docs
https://seu-dominio.com/docs  (se tiver domínio)
```

---

## 📊 Estrutura do Repo

Certifique-se que seu repositório tem:

```
WaterFalls-API/
├── app/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
├── migrations/
├── main.py
├── requirements.txt
├── Dockerfile          ← IMPORTANTE
├── .dockerignore       ← IMPORTANTE
└── .env.example
```

---

## 🆘 Se Algo Der Errado

### Container não sobe?

1. **Clique em "Logs"** no EasyPanel
2. Procure pela mensagem de erro
3. Problemas mais comuns:
   - ❌ Banco de dados inacessível → Verifique IP/porta/senha
   - ❌ Arquivo não encontrado → Verifique nomes de arquivo
   - ❌ Erro de import → Rodou `pip install -r requirements.txt`?

### Health Check falhando?

```bash
# Via SSH, teste manualmente:
curl http://localhost:8000/docs

# Veja logs:
docker logs waterfalls-api
```

### Migrations não rodaram?

```bash
docker exec waterfalls-api alembic upgrade head
```

---

## 🔄 Atualizar Código

1. Faça push para GitHub
2. No EasyPanel, clique **Redeploy**
3. EasyPanel vai puxar código novo e reiniciar

```bash
# Se mudou banco de dados:
docker exec waterfalls-api alembic upgrade head
```

---

## 📱 URLs da Sua API

Após deploy:

```
API Principal:           http://seu_ip:8000
Documentação Swagger:    http://seu_ip:8000/docs
ReDoc:                   http://seu_ip:8000/redoc

Ou com domínio:
https://seu-dominio.com
https://seu-dominio.com/docs
https://seu-dominio.com/redoc
```

---

## 💡 Dicas Importantes

✅ **Sempre use `DATABASE_URL`** completa nas variáveis
✅ **Certifique que banco está acessível** da VPS Hostinger
✅ **Use HTTPS** se tiver domínio (automático no EasyPanel)
✅ **Monitore logs** na primeira execução
✅ **Faça backup** dos dados regularmente
✅ **Atualize código** via Git, não manualmente

---

## 🎯 Checklist Rápido

- [ ] Dockerfile no repositório
- [ ] requirements.txt atualizado
- [ ] .dockerignore configurado
- [ ] Variáveis de ambiente corretas
- [ ] Banco de dados acessível
- [ ] Repositório no GitHub público
- [ ] EasyPanel apontando para branch `master`
- [ ] Container subiu (status green)
- [ ] API respondendo em `/docs`
- [ ] Migrations rodadas

---

## 🚀 Pronto!

Sua API está no ar e acessível 24/7 na Hostinger!

Qualquer dúvida, consulte:
- **EASYPANEL_GUIDE.md** - Guia detalhado
- **API_GUIDE.md** - Como usar a API
- **Logs do EasyPanel** - Mensagens de erro

---

**Desenvolvido para:** Hostinger EasyPanel  
**Última atualização:** Novembro 2024
