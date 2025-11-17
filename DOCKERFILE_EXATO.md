# 🐳 Dockerfile Exato para EasyPanel

**COPIE ESTE DOCKERFILE EXATAMENTE COMO ESTÁ:**

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

## ✅ Instruções para Colocar no EasyPanel

### Opção 1: Via GitHub (Recomendado)

1. Coloque este arquivo em: `./Dockerfile` (raiz do repositório)
2. Faça commit e push para GitHub
3. No EasyPanel:
   - Repository: `seu-usuario/WaterFalls-API`
   - Branch: `master`
   - Dockerfile: `./Dockerfile`
4. Clique **"Criar"**

### Opção 2: Upload Manual

1. Se usar upload na EasyPanel:
   - Crie arquivo chamado `Dockerfile` (sem extensão)
   - Cole o conteúdo acima
   - Salve na raiz do projeto
   - Faça upload na EasyPanel

---

## 🔑 Explicação do Dockerfile

### Por que Multi-Stage Build?
- **Reduz tamanho da imagem** (Builder descartado após build)
- **Mais rápido** para deployments futuros
- **Mais seguro** (dependências de build não incluídas)

### Linhas Importantes:

```dockerfile
FROM python:3.13-slim as builder
# → Imagem base compacta para compilar

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
# → Instala dependências sem cache (economiza espaço)

COPY --from=builder /root/.local /root/.local
# → Copia apenas os pacotes compilados para imagem final

ENV PATH=/root/.local/bin:$PATH
# → Aponta para Python instalado pelo pip

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1
# → EasyPanel verifica se aplicação está saudável

EXPOSE 8000
# → Abre porta 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# → Inicia a aplicação FastAPI
```

---

## ⚠️ Importante

1. **Não modifique este Dockerfile** - está otimizado para EasyPanel
2. **Mantenha no repositório** como `./Dockerfile` (sem extensão)
3. **requirements.txt deve estar na raiz** do projeto
4. **main.py deve estar na raiz** do projeto

---

## 🧪 Para Testar Localmente

Se quiser testar este Dockerfile antes de fazer deploy:

```bash
# Construir imagem
docker build -t waterfalls-api .

# Rodar container
docker run -d \
  --name waterfalls-test \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable \
  waterfalls-api

# Acessar
curl http://localhost:8000/docs

# Parar
docker stop waterfalls-test
docker rm waterfalls-test
```

---

## ✅ Checklist Antes de Deploy

- [ ] Dockerfile salvo como `./Dockerfile` (raiz do repo)
- [ ] requirements.txt existe e está atualizado
- [ ] main.py existe na raiz
- [ ] App rodando localmente (testado)
- [ ] Dockerfile no repositório Git
- [ ] GitHub repo é público OU EasyPanel tem acesso

---

## 🚀 Pronto!

Este Dockerfile é totalmente compatível com EasyPanel Hostinger.

Próximo passo: Coloque no EasyPanel seguindo `EASYPANEL_VISUAL.md`

---

**Última atualização:** Novembro 2024  
**Versão:** Production-ready  
**Status:** ✅ Testado
