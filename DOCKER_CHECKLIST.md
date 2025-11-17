# 🚢 Checklist de Deploy Docker - Hostinger VPS

## ✅ Antes de Fazer Deploy

- [ ] Você tem acesso SSH à sua VPS Hostinger
- [ ] Você tem o IP ou domínio da VPS
- [ ] Você conhece a senha SSH/root
- [ ] O banco de dados PostgreSQL está acessível (está em `31.97.170.13:5433`)
- [ ] Você tem o repositório Git pronto (ou arquivos prontos)

---

## ✅ Durante o Deploy

### Opção 1: Script Automático
- [ ] Conectou via SSH: `ssh root@seu_ip_vps`
- [ ] Baixou o script: `curl -O .../deploy.sh`
- [ ] Executou: `chmod +x deploy.sh && sudo ./deploy.sh`
- [ ] Respondeu as perguntas do script
- [ ] Verificou se a API está rodando: `docker-compose ps`

### Opção 2: Passo a Passo
- [ ] Conectou via SSH
- [ ] Instalou Docker: `curl -fsSL https://get.docker.com | sh`
- [ ] Instalou Docker Compose: `apt-get install -y docker-compose`
- [ ] Criou diretório: `mkdir -p /opt/WaterFalls-API && cd /opt/WaterFalls-API`
- [ ] Clonando repositório ou enviando arquivos
- [ ] Criou arquivo `.env` com variáveis
- [ ] Executou: `docker-compose up -d`
- [ ] Executou migrações: `docker-compose exec waterfalls-api alembic upgrade head`

---

## ✅ Após o Deploy

- [ ] API respondendo em `http://seu_ip:8000`
- [ ] Documentação acessível em `http://seu_ip:8000/docs`
- [ ] Testou um endpoint GET (listando endereços)
- [ ] Containers rodando: `docker-compose ps` mostra RUNNING
- [ ] Logs limpos: `docker-compose logs waterfalls-api` sem erros

---

## ✅ Configurações Opcionais (Recomendado)

### Nginx como Proxy Reverso
- [ ] Nginx instalado: `apt-get install -y nginx`
- [ ] Arquivo de configuração criado
- [ ] Site ativado: `ln -s /etc/nginx/sites-available/waterfalls /etc/nginx/sites-enabled/`
- [ ] Nginx testado: `nginx -t`
- [ ] Nginx reiniciado: `systemctl restart nginx`
- [ ] API acessível em: `http://seu_dominio.com`

### SSL/HTTPS com Certbot
- [ ] Certbot instalado: `apt-get install -y certbot python3-certbot-nginx`
- [ ] Certificado solicitado: `certbot --nginx -d seu_dominio.com`
- [ ] Certificado renovando automaticamente
- [ ] API acessível em: `https://seu_dominio.com`

---

## ✅ Monitoramento Básico

```bash
# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f waterfalls-api

# Usar de recursos
docker stats waterfalls-api

# Reiniciar se necessário
docker-compose restart
```

- [ ] Status verificado
- [ ] Logs consultados
- [ ] Recursos monitorados

---

## ✅ Backup & Recuperação

### Backup do Banco de Dados
```bash
# Fazer backup
docker-compose exec postgres pg_dump -U postgres water_falls > backup_$(date +%Y%m%d).sql

# Restaurar
docker-compose exec -T postgres psql -U postgres water_falls < backup.sql
```

- [ ] Backup regular agendado (cron job)
- [ ] Backup armazenado em local seguro
- [ ] Testou restauração de backup

---

## ✅ Manutenção Contínua

```bash
# Atualizar código
cd /opt/WaterFalls-API
git pull origin master
docker-compose build
docker-compose up -d
docker-compose exec waterfalls-api alembic upgrade head
```

- [ ] Configurou auto-update (opcional)
- [ ] Sabe como fazer rollback
- [ ] Documentou processo de atualização

---

## 📋 Documentação Importante

Você tem os seguintes arquivos:
- [ ] `Dockerfile` - Imagem da aplicação
- [ ] `docker-compose.yml` - Orquestração
- [ ] `.env.example` - Template de variáveis
- [ ] `DOCKER_DEPLOY.md` - Guia completo
- [ ] `DOCKER_QUICK.md` - Guia rápido
- [ ] `deploy.sh` - Script automático
- [ ] `requirements.txt` - Dependências Python

---

## 🚨 Troubleshooting

Se algo der errado:

1. **Verificar logs:**
   ```bash
   docker-compose logs waterfalls-api
   ```

2. **Verificar containers:**
   ```bash
   docker-compose ps
   ```

3. **Testar conexão BD:**
   ```bash
   docker-compose exec waterfalls-api python -c "
   from app.infrastructure.config.database import engine
   print('Conexão OK')
   "
   ```

4. **Reiniciar tudo:**
   ```bash
   docker-compose down
   docker-compose up -d
   docker-compose exec waterfalls-api alembic upgrade head
   ```

5. **Reconstruir (se mudar código):**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## ✨ Resultado Final

Após completar este checklist, você terá:

✅ API rodando 24/7 na VPS Hostinger
✅ Banco de dados remoto conectado
✅ Documentação Swagger acessível
✅ Domínio configurado (opcional)
✅ HTTPS/SSL ativo (opcional)
✅ Backup automático (recomendado)
✅ Monitoramento configurado
✅ Processo de atualização definido

---

## 📞 Suporte Rápido

**API não responde?**
```bash
curl -v http://seu_ip:8000/docs
docker-compose logs waterfalls-api
```

**Banco desconectado?**
```bash
docker-compose exec waterfalls-api python -c "from app.infrastructure.config.database import engine; engine.connect()"
```

**Porta 8000 em uso?**
```bash
lsof -i :8000
kill -9 <PID>
```

**Tudo quebrou?**
```bash
docker-compose down
docker-compose up -d
docker-compose exec waterfalls-api alembic upgrade head
```

---

## 🎉 Parabéns!

Sua API está no ar! Agora você pode:

1. Testar em: `http://seu_ip:8000/docs`
2. Compartilhar com o mundo: `http://seu_dominio.com`
3. Integrar com frontend
4. Fazer deploy de novas versões
5. Monitorar e manter a aplicação

---

**Última atualização:** Novembro 2024  
**Status:** ✅ Pronto para Produção
