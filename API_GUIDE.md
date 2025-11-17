# 📖 WaterFalls API - Guia Completo de Uso

API REST para gerenciamento de aluguel de veículos com arquitetura limpa (Clean Architecture).

---

## ⚡ Quick Start

### 1. Instalação
```bash
# Clone ou abra o projeto
cd WaterFalls-API

# Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### 2. Configuração
Crie arquivo `.env` na raiz:
```env
DATABASE_URL=postgresql://postgres:sua_senha@31.97.170.13:5433/water_falls?sslmode=disable
```

### 3. Migrações
```bash
cd migrations
alembic upgrade head
cd ..
```

### 4. Inicie o Servidor
```bash
python main.py
```

Pronto! Acesse: **http://127.0.0.1:8000/docs** 🎉

---

## 🔗 Endpoints Principais

### 📍 Endereços
```
POST   /enderecos/          Criar endereço
GET    /enderecos/          Listar todos
GET    /enderecos/{id}      Obter por ID
PUT    /enderecos/{id}      Atualizar
DELETE /enderecos/{id}      Deletar
```

### 🏪 Lojas
```
POST   /lojas/              Criar loja
GET    /lojas/              Listar todas
GET    /lojas/{id}          Obter por ID
PUT    /lojas/{id}          Atualizar
DELETE /lojas/{id}          Deletar
```

### 📦 Categorias de Veículos
```
POST   /categorias/         Criar categoria
GET    /categorias/         Listar todas
GET    /categorias/{id}     Obter por ID
PUT    /categorias/{id}     Atualizar
DELETE /categorias/{id}     Deletar
```

### 🚗 Veículos
```
POST   /veiculos/           Criar veículo
GET    /veiculos/           Listar todos
GET    /veiculos/{id}       Obter por ID
PUT    /veiculos/{id}       Atualizar
DELETE /veiculos/{id}       Deletar
```

### 👥 Clientes
```
POST   /clientes/           Criar cliente
GET    /clientes/           Listar todos
GET    /clientes/{id}       Obter por ID
PUT    /clientes/{id}       Atualizar
DELETE /clientes/{id}       Deletar
```

### 📅 Reservas
```
POST   /reservas/           Criar reserva
GET    /reservas/           Listar todas
GET    /reservas/{id}       Obter por ID
PUT    /reservas/{id}       Atualizar
DELETE /reservas/{id}       Deletar
```

### 💳 Pagamentos
```
POST   /pagamentos/         Criar pagamento
GET    /pagamentos/         Listar todos
GET    /pagamentos/{id}     Obter por ID
PUT    /pagamentos/{id}     Atualizar
GET    /pagamentos/?status=PAGO   Filtrar por status
```

### 📊 Histórico de Status
```
POST   /historico-status-veiculo/              Criar registro
GET    /historico-status-veiculo/              Listar todos
GET    /historico-status-veiculo/{id}         Obter por ID
GET    /historico-status-veiculo/veiculo/{id} Histórico de veículo
```

---

## 💡 Exemplos de Requisições

### 1️⃣ Criar Endereço
```bash
curl -X POST http://127.0.0.1:8000/enderecos/ \
  -H "Content-Type: application/json" \
  -d '{
    "rua": "Av. Paulista",
    "cidade": "São Paulo",
    "estado": "SP",
    "latitude": -23.5505,
    "longitude": -46.6333
  }'
```

**Resposta:**
```json
{
  "id": "uuid-aqui",
  "rua": "Av. Paulista",
  "cidade": "São Paulo",
  "estado": "SP",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "criado_em": "2024-11-17T10:30:00",
  "atualizado_em": "2024-11-17T10:30:00"
}
```

### 2️⃣ Criar Loja
```bash
curl -X POST http://127.0.0.1:8000/lojas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Loja Centro",
    "telefone": "1133334444",
    "endereco_id": "uuid-do-endereco"
  }'
```

### 3️⃣ Criar Categoria
```bash
curl -X POST http://127.0.0.1:8000/categorias/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "SUV"}'
```

### 4️⃣ Criar Veículo
```bash
curl -X POST http://127.0.0.1:8000/veiculos/ \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC1234",
    "marca": "Toyota",
    "modelo": "Corolla",
    "ano": 2023,
    "cor": "Branco",
    "combustivel": "Flex",
    "portas": 4,
    "cambio": "Automático",
    "quilometragem": 5000.0,
    "categoria_id": "uuid-categoria",
    "diaria": 150.0,
    "status": "DISPONIVEL",
    "loja_id": "uuid-loja",
    "image_url": "https://example.com/images/car-abc1234.jpg",
    "latitude": -23.5505,
    "longitude": -46.6333
  }'
```

### 5️⃣ Criar Cliente
```bash
curl -X POST http://127.0.0.1:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "telefone": "1199999999",
    "email": "joao@example.com",
    "endereco_id": "uuid-endereco",
    "cnh_numero": "123456789",
    "cnh_validade": "2030-12-31"
  }'
```

### 6️⃣ Criar Reserva
```bash
curl -X POST http://127.0.0.1:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "uuid-cliente",
    "veiculo_id": "uuid-veiculo",
    "loja_retirada_id": "uuid-loja",
    "loja_devolucao_id": "uuid-loja",
    "data_inicio": "2024-12-01",
    "data_fim": "2024-12-08",
    "periodo": 7,
    "valor_total": 1050.0,
    "motorista_incluido": false,
    "canal_origem": "WEB",
    "status": "CONFIRMADA"
  }'
```

### 7️⃣ Criar Pagamento
```bash
curl -X POST http://127.0.0.1:8000/pagamentos/ \
  -H "Content-Type: application/json" \
  -d '{
    "reserva_id": "uuid-reserva",
    "metodo": "CARTAO",
    "status": "PENDENTE",
    "valor": 1050.0,
    "transacao_gateway_id": "TRX123456"
  }'
```

### 8️⃣ Listar Todos os Endereços
```bash
curl -X GET http://127.0.0.1:8000/enderecos/
```

### 9️⃣ Obter Endereço por ID
```bash
curl -X GET http://127.0.0.1:8000/enderecos/uuid-aqui
```

### 🔟 Atualizar Endereço
```bash
curl -X PUT http://127.0.0.1:8000/enderecos/uuid-aqui \
  -H "Content-Type: application/json" \
  -d '{
    "rua": "Rua Nova",
    "cidade": "São Paulo",
    "estado": "SP"
  }'
```

### 1️⃣1️⃣ Deletar Endereço
```bash
curl -X DELETE http://127.0.0.1:8000/enderecos/uuid-aqui
```

### 1️⃣2️⃣ Filtrar Pagamentos por Status
```bash
curl -X GET "http://127.0.0.1:8000/pagamentos/?status=PAGO"
```

---

## 🗂️ Estrutura de Pastas

```
WaterFalls-API/
├── app/
│   ├── core/
│   │   └── config.py              # Configurações
│   ├── domain/                    # Entidades
│   │   ├── clientes.py
│   │   ├── lojas.py
│   │   ├── veiculos.py
│   │   └── reservas.py
│   ├── application/               # Serviços
│   │   ├── loja_service.py
│   │   ├── endereco_service.py
│   │   ├── pagamento_service.py
│   │   ├── veiculo_service.py
│   │   └── categoria_veiculo_service.py
│   ├── infrastructure/            # Repositories & ORM
│   │   ├── repositories/
│   │   │   ├── loja_repository.py
│   │   │   ├── endereco_repository.py
│   │   │   ├── pagamento_repository.py
│   │   │   ├── veiculo_repository.py
│   │   │   └── categoria_veiculo_repository.py
│   │   ├── models/
│   │   │   ├── loja_model.py
│   │   │   ├── endereco_model.py
│   │   │   ├── pagamento_model.py
│   │   │   └── veiculo_model.py
│   │   └── config/
│   │       └── database.py        # Conexão BD
│   └── presentation/              # Controllers
│       ├── loja_controller.py
│       ├── endereco_controller.py
│       ├── pagamento_controller.py
│       ├── veiculo_controller.py
│       └── categoria_veiculo_controller.py
├── migrations/                    # Alembic
│   ├── versions/
│   ├── alembic.ini
│   └── env.py
├── main.py                        # Entrada da App
├── requirements.txt               # Dependências
├── .env                          # Variáveis de ambiente
└── README.md                     # Este arquivo
```

---

## 📋 Dependências

```
fastapi==0.104.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
uvicorn==0.24.0
requests==2.31.0
```

---

## 🔍 Códigos HTTP

| Código | Significado |
|--------|-----------|
| **200** | OK - Sucesso |
| **201** | Created - Criado com sucesso |
| **204** | No Content - Deletado com sucesso |
| **400** | Bad Request - Dados inválidos |
| **404** | Not Found - Não encontrado |
| **422** | Unprocessable Entity - Erro de validação |
| **500** | Internal Server Error - Erro do servidor |

---

## 🧪 Testando a API

### Opção 1: Interface Swagger (Recomendado)
```
http://127.0.0.1:8000/docs
```

### Opção 2: ReDoc
```
http://127.0.0.1:8000/redoc
```

### Opção 3: Script Python
```bash
python test_all_cruds.py
```

---

## 📌 Padrões de Projeto

✅ **Clean Architecture** - Separação de responsabilidades em 4 camadas
✅ **Repository Pattern** - Abstração do banco de dados
✅ **Service Layer** - Lógica de negócio centralizada
✅ **DTOs (Pydantic)** - Validação de dados
✅ **Dependency Injection** - FastAPI Depends()
✅ **UUID** - Identificadores únicos em vez de IDs sequenciais
✅ **Migrations** - Alembic para versionamento do BD

---

## 🔐 Segurança (Próximos Passos)

- [ ] Autenticação JWT
- [ ] Autorização por roles
- [ ] Rate limiting
- [ ] CORS restritivo
- [ ] Validação de entrada robusta
- [ ] Hash de senhas

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação Swagger em `/docs`
2. Consulte os exemplos de requisição acima
3. Abra uma issue no repositório

---

**Última atualização:** Novembro 2024  
**Versão:** 1.0.0

