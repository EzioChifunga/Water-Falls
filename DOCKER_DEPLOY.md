# 🚀 Deploy no Hostinger com Docker

Guia passo a passo para fazer deploy da WaterFalls API na sua VPS do Hostinger.

---

## ✅ Pré-requisitos

- VPS Hostinger ativa
- Docker instalado na VPS
- Docker Compose instalado na VPS
- SSH acesso à VPS
- Git instalado (opcional, para clonar o repositório)

---

## 📋 Passo 1: Verificar se Docker está Instalado

Conecte via SSH à sua VPS:
```bash
ssh root@seu_ip_vps
```

Verifique se Docker está instalado:
```bash
docker --version
docker-compose --version
```

Se não estiver instalado, instale:
```bash
# Atualizar sistema
apt-get update && apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt-get install -y docker-compose
```

---

## 🔧 Passo 2: Clonar ou Enviar o Projeto

### Opção A: Via Git (Recomendado)
```bash
cd /opt
git clone https://github.com/seu-usuario/WaterFalls-API.git
cd WaterFalls-API
```

### Opção B: Via SCP (Se não usar Git)
No seu PC local:
```powershell
# Windows PowerShell
$files = Get-ChildItem -Path "C:\Users\ezioc\OneDrive\Área de Trabalho\Faculdade\WaterFalls-API" -Exclude "venv", "__pycache__", ".git"
foreach ($file in $files) {
    scp -r $file.FullName root@seu_ip_vps:/opt/WaterFalls-API/
}
```

---

## 🔐 Passo 3: Configurar Variáveis de Ambiente

Na VPS, crie o arquivo `.env`:
```bash
cd /opt/WaterFalls-API
nano .env
```

Cole este conteúdo (adapte com seus dados):
```env
# Se usar banco remoto (sua configuração atual)
DATABASE_URL=postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable

# Se usar banco local (PostgreSQL via Docker)
# DATABASE_URL=postgresql://postgres:sua_senha_forte@postgres:5432/water_falls
# DB_PASSWORD=sua_senha_forte
# DB_HOST=postgres
# DB_PORT=5432
# DB_NAME=water_falls

API_PORT=8000
```

Salve com: `CTRL+O`, `ENTER`, `CTRL+X`

---

## 🐳 Passo 4: Construir e Rodar com Docker Compose

### Para usar seu banco remoto (recomendado):
```bash
cd /opt/WaterFalls-API

# Construir imagem
docker-compose build

# Rodar em background
docker-compose up -d

# Ver logs
docker-compose logs -f waterfalls-api
```

### Para usar PostgreSQL local no Docker:
Edite o `.env` e descomente as linhas `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.

Depois:
```bash
docker-compose up -d
```

---

## ✨ Passo 5: Executar Migrações

Na primeira vez, execute as migrações:
```bash
docker-compose exec waterfalls-api alembic upgrade head
```

---

## 🌐 Passo 6: Acessar a API

A API estará disponível em:
```
http://seu_ip_vps:8000
http://seu_ip_vps:8000/docs (Swagger)
http://seu_ip_vps:8000/redoc (ReDoc)
```

Se sua VPS tem domínio, configure assim:
```
http://seu-dominio.com:8000
http://seu-dominio.com:8000/docs
```

---

## 🔒 Passo 7: Configurar Nginx (Opcional - Recomendado)

Para usar um domínio sem porta:

### Instale Nginx:
```bash
apt-get install -y nginx
```

### Crie arquivo de configuração:
```bash
nano /etc/nginx/sites-available/waterfalls
```

Cole:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;  # Troque pelo seu domínio

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### Ative a configuração:
```bash
ln -s /etc/nginx/sites-available/waterfalls /etc/nginx/sites-enabled/
nginx -t  # Testar configuração
systemctl restart nginx
```

Agora a API estará em: `http://seu-dominio.com/docs`

---

## 🔒 Passo 8: SSL/HTTPS com Certbot (Opcional - Recomendado)

```bash
apt-get install -y certbot python3-certbot-nginx

certbot --nginx -d seu-dominio.com
```

Certbot vai renovar automaticamente!

---

## 📊 Passo 9: Gerenciar Containers

### Ver status dos containers:
```bash
docker-compose ps
```

### Ver logs em tempo real:
```bash
docker-compose logs -f waterfalls-api
```

### Parar a aplicação:
```bash
docker-compose down
```

### Reiniciar a aplicação:
```bash
docker-compose restart
```

### Atualizar para nova versão:
```bash
git pull  # Se usar Git
docker-compose build
docker-compose up -d
docker-compose exec waterfalls-api alembic upgrade head
```

---

## 🧹 Limpeza e Manutenção

### Remover containers e volumes parados:
```bash
docker-compose down -v
```

### Limpar imagens não usadas:
```bash
docker image prune -a
```

### Ver uso de disco:
```bash
docker system df
```

---

## 🆘 Troubleshooting

### Problema: Porta 8000 já em uso
```bash
# Mudar porta no .env
API_PORT=9000

# Ou encontrar o processo:
lsof -i :8000
kill -9 <PID>
```

### Problema: Erro de conexão ao banco de dados
```bash
# Verificar logs
docker-compose logs waterfalls-api

# Testar conexão (dentro do container)
docker-compose exec waterfalls-api python -c "
from app.infrastructure.config.database import engine
engine.connect()
print('Conexão OK!')
"
```

### Problema: Container não sobe
```bash
# Ver erro detalhado
docker-compose build --no-cache
docker-compose up waterfalls-api  # Sem -d para ver logs
```

### Problema: Migrations falhando
```bash
# Rodar manualmente
docker-compose exec waterfalls-api bash
alembic upgrade head
```

---

## 📈 Monitoramento

### Verificar recursos (CPU, memória):
```bash
docker stats waterfalls-api
```

### Backup do banco de dados:
```bash
# Se usar PostgreSQL no Docker:
docker-compose exec postgres pg_dump -U postgres water_falls > backup.sql

# Restaurar:
docker-compose exec -T postgres psql -U postgres water_falls < backup.sql
```

---

## 🎯 Checklist Final

- ✅ Docker e Docker Compose instalados na VPS
- ✅ Projeto clonado/enviado para VPS
- ✅ `.env` configurado corretamente
- ✅ Containers rodando (`docker-compose up -d`)
- ✅ API acessível em `http://ip:8000/docs`
- ✅ Migrações executadas (`alembic upgrade head`)
- ✅ Nginx configurado (opcional)
- ✅ SSL/HTTPS ativo (opcional)

---

## 📞 Próximos Passos

1. **Testar a API**: Acesse `/docs` e teste um endpoint
2. **Configurar backup automático**: Use cron jobs
3. **Adicionar logs centralizados**: ELK Stack ou similar
4. **Monitoramento**: Prometheus + Grafana
5. **CI/CD**: GitHub Actions para deploy automático

---

**Suporte Hostinger:**
- Docs: https://support.hostinger.com/
- Tickets: https://www.hostinger.com/support

---

**Última atualização:** Novembro 2024
