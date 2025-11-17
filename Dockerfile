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
