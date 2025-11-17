# 🚀 Deploy WaterFalls API no EasyPanel (Hostinger)

Guia passo a passo para fazer deploy da API no EasyPanel da Hostinger.

---

## 📋 Pré-requisitos

✅ Conta Hostinger com EasyPanel ativo
✅ Repositório GitHub com o código da WaterFalls API
✅ Token de acesso ao GitHub (pessoal ou SSH)
✅ Domínio configurado (ou usar IP da VPS)

---

## 🔧 Passo 1: Acessar EasyPanel

1. Abra seu painel Hostinger: https://hpanel.hostinger.com
2. Vá para **Aplicações** → **EasyPanel**
3. Clique em **Criar Aplicação**

---

## 📝 Passo 2: Configurar Aplicação Docker

### 2.1 Informações Básicas

```
Nome da Aplicação: WaterFalls API
Descrição: API de aluguel de veículos
Tipo: Docker
```

### 2.2 Configurar Docker

**Opção A: Usando GitHub (Recomendado)**

```
Repositório: seu-usuario/WaterFalls-API
Branch: master
Dockerfile: ./Dockerfile
```

**Opção B: Fazer Upload Manual**

1. Baixe o repositório como ZIP
2. Faça upload dos arquivos no EasyPanel
3. Selecione o Dockerfile

---

## ⚙️ Passo 3: Variáveis de Ambiente

No EasyPanel, vá para **Variáveis de Ambiente** e adicione:

```env
DATABASE_URL=postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

**IMPORTANTE:** Certifique-se de que o banco de dados `31.97.170.13:5433` está acessível da VPS Hostinger.

---

## 🔌 Passo 4: Portas e Networking

No EasyPanel, configure as portas:

```
Porta Interna: 8000
Porta Externa: 8000 (ou deixe EasyPanel escolher)
```

Se usar domínio:
```
Domínio: seu-dominio.com
SSL: Ativo (Let's Encrypt automático)
```

---

## 📦 Passo 5: Volumes (Armazenamento)

Adicione volumes para persistência:

```
/app/migrations    → /data/migrations    (dados de migrações)
/app/logs          → /data/logs          (logs da aplicação)
```

---

## ✅ Passo 6: Revisar Configuração

Antes de criar, revise:

- ✅ Dockerfile correto
- ✅ Variáveis de ambiente configuradas
- ✅ Portas mapeadas
- ✅ Volumes configurados
- ✅ Banco de dados acessível

---

## 🚀 Passo 7: Criar e Deployar

1. Clique em **Criar Aplicação**
2. Aguarde a construção da imagem (pode levar 5-10 minutos)
3. EasyPanel vai iniciar o container automaticamente

---

## 📊 Monitorar Deployment

No EasyPanel:

1. Vá para **Aplicações** → **WaterFalls API**
2. Veja o status em tempo real
3. Consulte logs: **Logs** → **Container**
4. Se houver erro, veja a seção **Troubleshooting**

---

## ✨ Após Deploy Sucesso

### Acessar a API

```
http://seu_ip_vps:8000
http://seu_ip_vps:8000/docs        (Swagger)
http://seu_ip_vps:8000/redoc       (ReDoc)
```

Ou com domínio:
```
https://seu-dominio.com
https://seu-dominio.com/docs
https://seu-dominio.com/redoc
```

### Executar Migrações

Se for primeira vez, rode migrações:

No EasyPanel, vá para **Console** e execute:
```bash
alembic upgrade head
```

Ou via SSH:
```bash
docker exec waterfalls-api alembic upgrade head
```

### Testar um Endpoint

```bash
curl -X GET https://seu-dominio.com/docs
```

---

## 🔄 Atualizar Aplicação

### Se mudou o código no GitHub:

1. No EasyPanel, vá para **Aplicações** → **WaterFalls API**
2. Clique em **Redeploy** ou **Atualizar**
3. EasyPanel vai puxar código novo e reiniciar container

### Se mudou o banco de dados:

```bash
# Via SSH ou Console
docker exec waterfalls-api alembic upgrade head
```

---

## 🛑 Parar/Reiniciar Aplicação

No EasyPanel:

```
Parar:      Clique em "Stop"
Iniciar:    Clique em "Start"
Reiniciar:  Clique em "Restart"
```

---

## 📊 Monitoramento

EasyPanel oferece:

- ✅ **Logs em tempo real**: Veja o que está acontecendo
- ✅ **Health Check**: Verifica se aplicação está saudável
- ✅ **Restart automático**: Reinicia se cair
- ✅ **CPU/Memória**: Monitora recursos
- ✅ **Backups**: Automáticos do código

---

## 🆘 Troubleshooting

### Container não sobe

**Verificar logs:**
```
No EasyPanel → Logs → veja mensagens de erro
```

**Problemas comuns:**
- ❌ Banco de dados inacessível: Verifique `DATABASE_URL`
- ❌ Porta em uso: Mude porta externa no EasyPanel
- ❌ Falta memória: Aumente recursos no painel

### Erro de conexão ao banco

Verifique:
```bash
# Conecte via SSH e teste:
docker exec waterfalls-api python -c "
from app.infrastructure.config.database import engine
print('Conexão OK')
"
```

Se falhar, verifique:
1. IP do banco (`31.97.170.13:5433`)
2. Credenciais do banco (usuário/senha)
3. Se firewall permite conexão da VPS ao banco

### API não responde

```bash
# Verificar se container está rodando:
docker ps | grep waterfalls

# Ver status no EasyPanel:
Vá para Health Check
```

### Migrations não rodaram

```bash
# No Console EasyPanel:
alembic upgrade head

# Ou via SSH:
docker exec waterfalls-api alembic upgrade head
```

---

## 💾 Backup e Recuperação

### Backup do código:
- EasyPanel faz automaticamente
- GitHub também tem seu código

### Backup do banco de dados:
```bash
# Via SSH
docker exec waterfalls-api pg_dump -h 31.97.170.13 -U postgres -d water_falls > backup.sql

# Ou fazer backup via Hostinger Hpanel se tiver BD lá
```

---

## 🔐 Segurança

✅ **HTTPS automático**: EasyPanel usa Let's Encrypt
✅ **Firewall**: Configure no painel Hostinger
✅ **Variáveis sensíveis**: Use Environment Variables, não hardcode
✅ **Updates regulares**: Mantenha Python atualizado

---

## 📱 Integração com Frontend

Sua API está acessível em:
```
https://seu-dominio.com/api
```

Configure CORS se necessário no `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Performance

### Melhorar performance:

1. **Cache**: Adicione Redis (se disponível)
2. **CDN**: Use Cloudflare (grátis)
3. **Compress**: FastAPI comprime automaticamente
4. **Async**: Use async/await nos endpoints

### Monitorar performance:

- Veja tempo de resposta em `/docs`
- Use Chrome DevTools para debugar
- Monitore CPU/Memória no EasyPanel

---

## 🎯 Próximos Passos

1. ✅ Testar endpoints em `/docs`
2. ✅ Compartilhar URL com equipe
3. ✅ Integrar com frontend
4. ✅ Configurar domínio customizado
5. ✅ Adicionar monitoramento extra

---

## 📞 Suporte

**Problemas com EasyPanel:**
- Hostinger Suporte: https://support.hostinger.com/
- Tickets: https://www.hostinger.com/support

**Problemas com API:**
- Consulte `API_GUIDE.md`
- Veja logs no EasyPanel
- Teste endpoints em `/docs`

---

## ✅ Checklist Final

- [ ] Aplicação criada no EasyPanel
- [ ] Variáveis de ambiente configuradas
- [ ] Container subiu com sucesso
- [ ] Health check passando
- [ ] Migrations rodadas (`alembic upgrade head`)
- [ ] API respondendo em `/docs`
- [ ] Domínio configurado
- [ ] HTTPS ativo
- [ ] Logs sendo monitorados

---

**Pronto para produção!** 🚀

Sua WaterFalls API está no ar e acessível 24/7!

---

**Última atualização:** Novembro 2024  
**Compatível com:** EasyPanel Hostinger
