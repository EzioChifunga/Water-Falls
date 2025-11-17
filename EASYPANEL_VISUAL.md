# 🖼️ Guia Visual - EasyPanel Hostinger

Siga os passos visuais para fazer deploy no EasyPanel.

---

## 📍 PASSO 1: Acessar EasyPanel

1. Acesse: https://hpanel.hostinger.com
2. Faça login com suas credenciais Hostinger
3. No menu lateral, procure por **"Aplicações"** ou **"Applications"**
4. Clique em **"EasyPanel"**

---

## 📍 PASSO 2: Criar Nova Aplicação

1. Clique em botão **"Criar Aplicação"** ou **"New Application"** (verde)
2. Escolha **"Docker"** como tipo de aplicação
3. Clique **"Próximo"** ou **"Next"**

---

## 📍 PASSO 3: Configurar Repositório GitHub

### Campo: Repository (Repositório)
```
seu-usuario/WaterFalls-API
```

### Campo: Branch
```
master
```

### Campo: Dockerfile Path
```
./Dockerfile
```

**Ou se preferir upload manual:**
1. Clique em "Upload Files" em vez de GitHub
2. Faça upload dos arquivos do projeto
3. Certifique que `Dockerfile` está na raiz

---

## 📍 PASSO 4: Variáveis de Ambiente

1. Procure por aba **"Environment Variables"** ou **"Variáveis de Ambiente"**
2. Clique em **"Adicionar Variável"** ou **"Add Variable"**

### Adicione estas variáveis (UMA POR UMA):

**Variável 1:**
```
Nome: DATABASE_URL
Valor: postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable
```

**Variável 2:**
```
Nome: PYTHONUNBUFFERED
Valor: 1
```

**Variável 3:**
```
Nome: PYTHONDONTWRITEBYTECODE
Valor: 1
```

---

## 📍 PASSO 5: Configurar Portas

1. Procure por aba **"Ports"** ou **"Portas"**

### Campo: Internal Port (Porta Interna)
```
8000
```

### Campo: External Port (Porta Externa)
```
8000
(ou deixe vazio para EasyPanel escolher automaticamente)
```

---

## 📍 PASSO 6: Domínio (Opcional)

Se quiser usar um domínio:

1. Procure por aba **"Domains"** ou **"Domínios"**
2. Clique em **"Adicionar Domínio"**
3. Digite seu domínio: `seu-dominio.com`
4. Ative **"SSL"** (Let's Encrypt automático)

---

## 📍 PASSO 7: Volumes (Opcional)

Se quiser persistir dados:

1. Procure por aba **"Volumes"** ou **"Volumes"**
2. Adicione:

**Volume 1:**
```
Container Path: /app/migrations
Host Path: /data/migrations
```

**Volume 2:**
```
Container Path: /app/logs
Host Path: /data/logs
```

---

## 📍 PASSO 8: Revisar e Criar

1. Revise todas as configurações
2. Clique em **"Criar"** ou **"Create"**
3. Aguarde a construção (5-10 minutos)

**Status esperado:**
- ✅ Building... → Building image
- ✅ Starting... → Inicializando container
- ✅ Running... → Aplicação rodando

---

## 📍 PASSO 9: Verificar Status

1. Acesse a aplicação no painel
2. Procure por **"Health Check"**
3. Status deve ser: ✅ **GREEN** (Saudável)

Se for 🔴 **RED** (com problema):
- Clique em **"Logs"**
- Veja a mensagem de erro
- Consulte seção **Troubleshooting** abaixo

---

## 📍 PASSO 10: Acessar a API

### Opção A: Via IP
```
http://seu_ip_vps:8000
http://seu_ip_vps:8000/docs        (Documentação)
```

### Opção B: Via Domínio (se configurou)
```
https://seu-dominio.com
https://seu-dominio.com/docs       (Documentação)
```

---

## 📍 PASSO 11: Rodar Migrations (IMPORTANTE!)

**Primeira vez após criar:**

1. No painel do EasyPanel, procure por **"Console"** ou **"SSH"**
2. Execute este comando:

```bash
docker exec waterfalls-api alembic upgrade head
```

Aguarde completar. Você verá:
```
...
INFO  [alembic.runtime.migration] Running upgrade... done
```

---

## 🆘 TROUBLESHOOTING

### ❌ Container Status: RED / Unhealthy

**Causa:** Erro na inicialização

**Solução:**
1. Clique em **"Logs"**
2. Procure pela linha de erro
3. Verifique:
   - DATABASE_URL está correto?
   - Porta 8000 está livre?
   - Banco de dados está acessível?

### ❌ "Connection refused"

**Causa:** Banco de dados não está acessível

**Solução:**
1. Verifique DATABASE_URL:
   ```
   postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable
   ```
2. Verifique se firewall permite conexão
3. Teste conexão via SSH:
   ```bash
   docker exec waterfalls-api python -c "
   from app.infrastructure.config.database import engine
   print('OK')
   "
   ```

### ❌ "Module not found"

**Causa:** Faltam dependências

**Solução:**
1. Verifique se `requirements.txt` está na raiz do repositório
2. Clique em **"Redeploy"** para reconstruir
3. Aguarde rebuildar

### ❌ API respondendo mas dando 500 error

**Causa:** Migrations não rodadas

**Solução:**
```bash
docker exec waterfalls-api alembic upgrade head
```

---

## 🔄 ATUALIZAR CÓDIGO

Quando você fizer push para GitHub:

1. No painel EasyPanel
2. Clique em **"Redeploy"** ou **"Atualizar"**
3. EasyPanel vai:
   - Puxar código novo
   - Reconstruir imagem
   - Reiniciar container

**Se mudou banco de dados:**
```bash
docker exec waterfalls-api alembic upgrade head
```

---

## 📊 MONITORAR APLICAÇÃO

No painel EasyPanel você pode:

- ✅ **Logs:** Ver logs em tempo real
- ✅ **Health Check:** Status da aplicação
- ✅ **Restart:** Reiniciar container
- ✅ **Stop/Start:** Pausar e retomar
- ✅ **Redeploy:** Atualizar código

---

## 🧪 TESTAR A API

Após deploy bem-sucedido:

```bash
# Teste um endpoint
curl -X GET https://seu-dominio.com/enderecos/

# Ou acesse no navegador:
https://seu-dominio.com/docs
```

Deve aparecer:
- Documentação Swagger interativa
- Lista de todos os endpoints
- Botão "Try it out" para testar

---

## ✅ CHECKLIST FINAL

- [ ] Repositório no GitHub
- [ ] Dockerfile na raiz
- [ ] requirements.txt na raiz
- [ ] Variáveis de ambiente corretas
- [ ] Container status: GREEN ✅
- [ ] Health Check: GREEN ✅
- [ ] Migrations rodadas
- [ ] API respondendo em `/docs`
- [ ] Domínio configurado (se tiver)
- [ ] SSL ativo (se tiver domínio)

---

## 🎉 PRONTO!

Sua API está no ar 24/7!

```
✅ URL: https://seu-dominio.com
✅ Docs: https://seu-dominio.com/docs
✅ Status: Running
```

---

## 📞 PRECISA DE AJUDA?

1. **Consulte os logs:** EasyPanel → Logs
2. **Leia a documentação:** EASYPANEL_GUIDE.md
3. **Teste a API:** /docs (Swagger)
4. **Suporte Hostinger:** support.hostinger.com

---

**Última atualização:** Novembro 2024  
**Compatível com:** Hostinger EasyPanel
