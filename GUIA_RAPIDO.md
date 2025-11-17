# 🚀 Guia de Início Rápido - WaterFalls API

## Prerequisites

- Python 3.13+
- PostgreSQL 12+
- Git
- Postman (opcional, para testes)

---

## 1️⃣ Clonar/Abrir Projeto

```bash
cd "c:\Users\ezioc\OneDrive\Área de Trabalho\Faculdade\WaterFalls-API"
```

---

## 2️⃣ Criar Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (CMD)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar Banco de Dados

### Criar arquivo `.env`

```env
# Database Configuration
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha_postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=water_falls
DATABASE_SSLMODE=disable

# API Configuration
API_TITLE=WaterFalls API
API_VERSION=1.0.0
API_DESCRIPTION=API para gerenciamento de carros

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Criar banco de dados PostgreSQL

```sql
CREATE DATABASE water_falls;
```

---

## 5️⃣ Executar Migrações

### Criar tabelas iniciais
```bash
python -m alembic upgrade head
```

### Verificar status das migrações
```bash
python -m alembic current
```

### Ver histórico de migrações
```bash
python -m alembic history
```

---

## 6️⃣ Iniciar Servidor

### Desenvolvimento (com reload automático)
```bash
python main.py
```

### Ou usando uvicorn diretamente
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Saída esperada:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Application startup complete
```

---

## 7️⃣ Acessar a API

### Documentação Swagger (Recomendado)
```
http://localhost:8000/docs
```

### Documentação ReDoc (Alternativo)
```
http://localhost:8000/redoc
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Raiz da API
```bash
curl http://localhost:8000/
```

---

## 8️⃣ Testar Endpoints

### Exemplo: Criar um Carro

```bash
curl -X POST "http://localhost:8000/cars/" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2023,
    "color": "Branco",
    "plate": "ABC1234"
  }'
```

### Exemplo: Listar Carros

```bash
curl -X GET "http://localhost:8000/cars/?skip=0&limit=10"
```

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'app'"

**Solução**: Certifique-se de estar na raiz do projeto
```bash
cd "c:\Users\ezioc\OneDrive\Área de Trabalho\Faculdade\WaterFalls-API"
python main.py
```

### Erro: "could not connect to server"

**Solução**: Verifique se PostgreSQL está rodando
```bash
# Windows
net start postgresql-x64-15

# Linux
sudo systemctl start postgresql

# Mac
brew services start postgresql@14
```

### Erro: "FATAL: database does not exist"

**Solução**: Crie o banco de dados
```bash
python -m alembic upgrade head
```

### Erro: "ImportError" ao rodar migrations

**Solução**: Reinstale as dependências
```bash
pip install -r requirements.txt --force-reinstall
python -m alembic upgrade head
```

### Porta 8000 já em uso

**Solução**: Use outra porta
```bash
uvicorn main:app --reload --port 8001
```

---

## 📚 Estrutura de Pastas

```
WaterFalls-API/
├── app/
│   ├── core/               # Config e Database
│   ├── domain/             # Entidades
│   ├── infrastructure/     # ORM e Repositories
│   └── presentation/       # Rotas
├── migrations/             # Alembic migrations
├── main.py                 # Entry point
├── requirements.txt        # Dependências
├── alembic.ini            # Config Alembic
├── .env                   # Variáveis de ambiente
├── .gitignore             # Git ignore
├── README.md              # Documentação principal
├── DIAGRAMA_DB.md         # Diagrama de banco de dados
├── EXEMPLOS_REQUISICOES.md # Exemplos de uso
├── CHECKLIST.md           # Checklist de implementação
└── GUIA_RAPIDO.md         # Este arquivo
```

---

## 📖 Documentação Completa

- **README.md** - Visão geral do projeto
- **DIAGRAMA_DB.md** - Relacionamentos e tabelas
- **EXEMPLOS_REQUISICOES.md** - Exemplos de requisições HTTP
- **CHECKLIST.md** - Checklist de implementação

---

## 🧪 Testando com Postman

1. Abra Postman
2. Clique em **New → Request**
3. Configure:
   - **Method**: POST
   - **URL**: http://localhost:8000/cars/
   - **Headers**: Content-Type: application/json
   - **Body** (raw JSON):
   ```json
   {
     "brand": "Honda",
     "model": "Civic",
     "year": 2023,
     "color": "Preto",
     "plate": "XYZ9999"
   }
   ```
4. Clique **Send**

---

## 🎓 Aprendendo a API

### 1. Comece pela documentação Swagger
```
http://localhost:8000/docs
```

### 2. Teste endpoints simples primeiro
- GET /health
- GET /cars/
- POST /cars/

### 3. Leia os exemplos
- Veja EXEMPLOS_REQUISICOES.md

### 4. Estude o diagrama de banco de dados
- Veja DIAGRAMA_DB.md

---

## 🐛 Debugging

### Ativar logs detalhados

```python
# Em main.py, adicione:
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Ver queries SQL geradas

```python
# Em app/core/database.py, altere:
engine = create_engine(DATABASE_URL, echo=True)  # echo=True ativa logging de SQL
```

---

## 📊 Exemplo de Fluxo Completo

### 1. Verificar saúde da API
```bash
curl http://localhost:8000/health
```

### 2. Criar um carro
```bash
curl -X POST "http://localhost:8000/cars/" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2023,
    "color": "Branco",
    "plate": "ABC1234"
  }'
```

### 3. Listar carros
```bash
curl "http://localhost:8000/cars/"
```

### 4. Obter um carro específico
```bash
curl "http://localhost:8000/cars/1"
```

### 5. Atualizar um carro
```bash
curl -X PUT "http://localhost:8000/cars/1" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Honda",
    "model": "Civic",
    "year": 2024,
    "color": "Preto",
    "plate": "ABC1234"
  }'
```

### 6. Deletar um carro
```bash
curl -X DELETE "http://localhost:8000/cars/1"
```

---

## 🚀 Deployment (Futuro)

### Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: water_falls
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/water_falls
    depends_on:
      - db
```

---

## 📞 Suporte

Em caso de dúvidas:
1. Consulte README.md
2. Consulte DIAGRAMA_DB.md
3. Veja EXEMPLOS_REQUISICOES.md
4. Acesse /docs para documentação interativa

---

## ✨ Bom uso!

A API está pronta para uso. Explore os endpoints e aproveite! 🚀
