# 🐳 Deploy Docker - Guia Rápido para Hostinger

## 3 Formas de Fazer Deploy

### ⚡ Forma 1: Script Automático (RECOMENDADO)

```bash
# Na sua VPS via SSH:
ssh root@seu_ip_vps

# Baixe e execute o script:
curl -O https://raw.githubusercontent.com/seu-usuario/WaterFalls-API/master/deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh
```

O script vai:
- ✅ Instalar Docker e Docker Compose
- ✅ Clonar seu repositório
- ✅ Configurar variáveis de ambiente
- ✅ Rodar a API
- ✅ Configurar Nginx (opcional)
- ✅ Configurar SSL (opcional)

**Tempo total:** ~5 minutos

---

### 📋 Forma 2: Passo a Passo Manual

```bash
# 1. Conectar via SSH
ssh root@seu_ip_vps

# 2. Instalar Docker (se não tiver)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt-get install -y docker-compose

# 3. Clonar projeto
cd /opt
git clone https://github.com/seu-usuario/WaterFalls-API.git
cd WaterFalls-API

# 4. Configurar .env
nano .env
# Cole:
# DATABASE_URL=postgresql://postgres:sua_senha@31.97.170.13:5433/water_falls?sslmode=disable
# API_PORT=8000

# 5. Rodar Docker Compose
docker-compose up -d

# 6. Executar migrações
docker-compose exec waterfalls-api alembic upgrade head

# 7. Pronto! Acesse:
# http://seu_ip_vps:8000/docs
```

---

### 🖥️ Forma 3: Docker Manual (Sem Compose)

```bash
# Construir imagem
docker build -t waterfalls-api .

# Rodar container
docker run -d \
  --name waterfalls-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  waterfalls-api

# Ver logs
docker logs -f waterfalls-api
```

---

## 📁 Arquivos Inclusos

```
Dockerfile          - Imagem Docker da aplicação
docker-compose.yml  - Orquestração de containers
.dockerignore       - Arquivos a ignorar no Docker
.env.example        - Exemplo de variáveis
deploy.sh           - Script de deploy automático
DOCKER_DEPLOY.md    - Guia completo de deploy
```

---

## 🔑 Variáveis de Ambiente

Crie arquivo `.env` na VPS:

```env
# Banco de dados remoto (sua situação atual)
DATABASE_URL=postgresql://postgres:sua_senha@31.97.170.13:5433/water_falls?sslmode=disable

# Ou banco local com Docker:
# DATABASE_URL=postgresql://postgres:sua_senha@postgres:5432/water_falls
# DB_PASSWORD=sua_senha
# DB_HOST=postgres
# DB_PORT=5432
# DB_NAME=water_falls

# Porta da API
API_PORT=8000
```

---

## 🚀 Após o Deploy

### Verificar se está rodando:
```bash
docker-compose ps
docker-compose logs -f waterfalls-api
```

### Acessar documentação:
```
http://seu_ip_vps:8000/docs
http://seu_ip_vps:8000/redoc
```

### Testar um endpoint:
```bash
curl -X GET http://seu_ip_vps:8000/enderecos/
```

---

## 🔄 Atualizar Aplicação

```bash
cd /opt/WaterFalls-API

# Puxar novo código
git pull origin master

# Reconstruir imagem
docker-compose build

# Reiniciar containers
docker-compose up -d

# Rodar migrações se houver mudanças no BD
docker-compose exec waterfalls-api alembic upgrade head
```

---

## 🛑 Parar a Aplicação

```bash
docker-compose down
```

---

## 🧹 Remover Tudo

```bash
# Parar containers
docker-compose down -v

# Remover imagem
docker rmi waterfalls-api
```

---

## 🆘 Problemas Comuns

### Porta 8000 em uso?
```bash
lsof -i :8000
kill -9 <PID>
```

### Container não sobe?
```bash
docker-compose logs waterfalls-api
```

### Erro de conexão ao BD?
```bash
docker-compose exec waterfalls-api python -c "
from app.infrastructure.config.database import engine
print(engine.connect())
"
```

---

## 💡 Dicas

1. **Use seu banco remoto atual**: Não precisa rodar PostgreSQL no Docker, use o que já está em `31.97.170.13:5433`

2. **Nginx como proxy**: Para usar domínio sem porta, configure Nginx

3. **Certificado SSL**: Use Certbot para HTTPS automático

4. **Backups**: Backup regular do PostgreSQL

5. **Monitoring**: Use `docker stats` para monitorar recursos

---

## 📞 Suporte

- Logs completos: `docker-compose logs waterfalls-api`
- Arquivo completo: Ver `DOCKER_DEPLOY.md`

---

**Pronto para fazer deploy!** 🚀
