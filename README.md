# WaterFalls API - Sistema de Aluguel de Veículos

## 📋 Resumo do Projeto

API REST completa para gerenciamento de aluguel de veículos, desenvolvida com FastAPI, SQLAlchemy e PostgreSQL.

### Arquitetura: Clean Architecture com 4 Camadas

```
app/
├── domain/          # Entidades de domínio (Business Logic)
├── application/     # Serviços de aplicação (Use Cases)
├── infrastructure/  # ORM, Repositórios, Config
└── presentation/    # Rotas/Controllers (FastAPI)
```

---

## 📊 Banco de Dados

### Tabelas Criadas

#### 1. **cars** (Sistema Original)
- Tabela simples para testes
- Campos: id, brand, model, year, color, plate

#### 2. **enderecos** (Reutilizável)
- `id` (UUID PK)
- `rua`, `cidade`, `estado` (VARCHAR)
- `latitude`, `longitude` (DECIMAL)

#### 3. **clientes**
- `id` (UUID PK)
- `nome`, `cpf` (UNIQUE), `telefone`, `email` (UNIQUE)
- `endereco_id` (FK → enderecos)
- `cnh_numero`, `cnh_validade` (DATE)
- `criado_em`, `atualizado_em` (TIMESTAMP)

#### 4. **categorias_veiculos**
- `id` (UUID PK)
- `nome` (VARCHAR UNIQUE)
- Exemplos: econômico, sedan, SUV, luxo

#### 5. **lojas**
- `id` (UUID PK)
- `nome`, `telefone`
- `endereco_id` (FK → enderecos)

#### 6. **veiculos**
- `id` (UUID PK)
- `placa` (CHAR(7) UNIQUE)
- `marca`, `modelo`, `ano`
- `categoria_id` (FK → categorias_veiculos)
- `diaria` (NUMERIC(10,2))
- `status` (ENUM: DISPONIVEL, ALUGADO, RESERVADO, MANUTENCAO, FORA_AREA)
- `loja_id` (FK → lojas)
- `latitude`, `longitude` (para rastreamento)
- `criado_em`, `atualizado_em`

#### 7. **reservas**
- `id` (UUID PK)
- `cliente_id` (FK), `veiculo_id` (FK)
- `loja_retirada_id`, `loja_devolucao_id` (FK → lojas)
- `data_inicio`, `data_fim` (DATE)
- `periodo` (SMALLINT: 7, 15, 30 dias)
- `valor_total` (NUMERIC)
- `motorista_incluido` (BOOLEAN)
- `canal_origem` (ENUM: WEB, LOJA, TELEFONE)
- `status` (ENUM: PENDENTE_PAGAMENTO, CONFIRMADA, EM_CURSO, FINALIZADA, CANCELADA)
- `criado_em`, `atualizado_em`

#### 8. **pagamentos**
- `id` (UUID PK)
- `reserva_id` (FK UNIQUE → reservas)
- `metodo` (ENUM: CARTAO)
- `status` (ENUM: PAGO, PENDENTE, RECUSADO)
- `valor` (NUMERIC)
- `transacao_gateway_id` (VARCHAR UNIQUE, opcional)
- `criado_em`

#### 9. **historico_status_veiculo** (Auditoria)
- `id` (UUID PK)
- `veiculo_id` (FK)
- `status_anterior`, `status_atual` (ENUM)
- `data_mudanca` (TIMESTAMP)

---

## 🚀 Funcionalidades Implementadas

### CRUD de Carros (Sistema Original)
- ✅ POST `/cars/` - Criar carro
- ✅ GET `/cars/` - Listar carros (com paginação)
- ✅ GET `/cars/{id}` - Obter carro
- ✅ PUT `/cars/{id}` - Atualizar carro
- ✅ DELETE `/cars/{id}` - Deletar carro

### CRUD de Clientes
- ✅ POST `/clientes/` - Criar cliente
- ✅ GET `/clientes/` - Listar clientes (com paginação)
- ✅ GET `/clientes/{id}` - Obter cliente
- ✅ PUT `/clientes/{id}` - Atualizar cliente
- ✅ DELETE `/clientes/{id}` - Deletar cliente

### CRUD de Veículos
- ✅ POST `/veiculos/` - Criar veículo
- ✅ GET `/veiculos/` - Listar todos
- ✅ GET `/veiculos/{id}` - Obter veículo
- ✅ GET `/veiculos/placa/{placa}` - Buscar por placa
- ✅ GET `/veiculos/loja/{loja_id}` - Veículos de uma loja
- ✅ GET `/veiculos/disponveis` - Apenas disponíveis
- ✅ PUT `/veiculos/{id}` - Atualizar veículo
- ✅ PATCH `/veiculos/{id}/status` - Atualizar status
- ✅ DELETE `/veiculos/{id}` - Deletar veículo

### CRUD de Reservas
- ✅ POST `/reservas/` - Criar reserva
- ✅ GET `/reservas/` - Listar reservas
- ✅ GET `/reservas/{id}` - Obter reserva
- ✅ GET `/reservas/cliente/{cliente_id}` - Reservas do cliente
- ✅ GET `/reservas/veiculo/{veiculo_id}` - Reservas do veículo
- ✅ PATCH `/reservas/{id}/confirmar` - Confirmar reserva
- ✅ PATCH `/reservas/{id}/cancelar` - Cancelar reserva
- ✅ DELETE `/reservas/{id}` - Deletar reserva

---

## 📁 Estrutura de Arquivos

```
app/
├── core/
│   ├── config.py           # Configurações (Pydantic)
│   ├── database.py         # Conexão BD
│   └── __init__.py
│
├── domain/                 # Entidades (Business Logic)
│   ├── cars.py
│   ├── clientes.py
│   ├── veiculos.py
│   ├── lojas.py
│   ├── reservas.py
│   └── __init__.py
│
├── infrastructure/
│   ├── config/
│   │   └── database.py     # SQLAlchemy config
│   │
│   ├── models/             # ORM (SQLAlchemy)
│   │   ├── car_model.py
│   │   ├── cliente_model.py
│   │   ├── veiculo_model.py
│   │   ├── categoria_veiculo_model.py
│   │   ├── loja_model.py
│   │   ├── endereco_model.py
│   │   ├── reserva_model.py
│   │   ├── pagamento_model.py
│   │   ├── historico_status_veiculo_model.py
│   │   └── __init__.py
│   │
│   └── repositories/       # Data Access
│       ├── car_repository.py
│       ├── cliente_repository.py
│       ├── veiculo_repository.py
│       ├── categoria_veiculo_repository.py
│       ├── loja_repository.py
│       ├── endereco_repository.py
│       ├── reserva_repository.py
│       ├── pagamento_repository.py
│       └── __init__.py
│
├── application/            # Use Cases/Services
│   ├── car_service.py
│   ├── cliente_service.py
│   ├── veiculo_service.py
│   ├── reserva_service.py
│   └── __init__.py
│
└── presentation/           # API Endpoints
    ├── car_controller.py
    ├── cliente_controller.py
    ├── veiculo_controller.py
    ├── reserva_controller.py
    └── __init__.py

main.py                    # Entry point FastAPI
migrations/                # Alembic migrations
requirements.txt           # Dependências
alembic.ini               # Config Alembic
.env                      # Variáveis de ambiente
```

---

## 🛠️ Instalação

### 1. Criar Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar .env
```env
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=seu_host
DATABASE_PORT=5433
DATABASE_NAME=water_falls
DATABASE_SSLMODE=disable
```

### 4. Executar Migrações
```bash
python -m alembic upgrade head
```

### 5. Iniciar Servidor
```bash
python main.py
```

Acesse: http://localhost:8000/docs

---

## 🔗 Endpoints

### Root
- `GET /` - Info da API
- `GET /health` - Health check

### Cars (Sistema Original)
- `POST /cars/`
- `GET /cars/`
- `GET /cars/{id}`
- `PUT /cars/{id}`
- `DELETE /cars/{id}`

### Clientes
- `POST /clientes/`
- `GET /clientes/`
- `GET /clientes/{cliente_id}`
- `PUT /clientes/{cliente_id}`
- `DELETE /clientes/{cliente_id}`

### Veículos
- `POST /veiculos/`
- `GET /veiculos/`
- `GET /veiculos/{veiculo_id}`
- `GET /veiculos/placa/{placa}`
- `GET /veiculos/loja/{loja_id}`
- `GET /veiculos/disponveis`
- `PUT /veiculos/{veiculo_id}`
- `PATCH /veiculos/{veiculo_id}/status`
- `DELETE /veiculos/{veiculo_id}`

### Reservas
- `POST /reservas/`
- `GET /reservas/`
- `GET /reservas/{reserva_id}`
- `GET /reservas/cliente/{cliente_id}`
- `GET /reservas/veiculo/{veiculo_id}`
- `PATCH /reservas/{reserva_id}/confirmar`
- `PATCH /reservas/{reserva_id}/cancelar`
- `DELETE /reservas/{reserva_id}`

---

## 💡 Padrões Utilizados

✅ **Clean Architecture** - Separação de responsabilidades
✅ **Repository Pattern** - Abstração do banco de dados
✅ **Service Layer** - Lógica de negócio
✅ **DTOs (Pydantic)** - Validação de entrada/saída
✅ **Dependency Injection** - FastAPI Depends
✅ **Migrations** - Alembic para versionamento de BD
✅ **CRUD Completo** - POST, GET, PUT, DELETE
✅ **Paginação** - Em endpoints de listagem
✅ **UUIDs** - Identificadores únicos
✅ **Enums** - Tipos seguros de status

---

## 📝 Notas Importantes

1. **UUID vs Integer ID**: Usamos UUID para novas tabelas (cliente, veículo, etc.) e Integer apenas para a tabela cars legada
2. **Timestamps**: Todos os modelos tem `criado_em` e `atualizado_em`
3. **Constraints**: CHECK para período de reserva (7, 15, 30)
4. **Foreign Keys**: Relacionamentos bem definidos
5. **Enums**: Usando ENUM do PostgreSQL para status
6. **Migrações**: Versionadas com Alembic para rastreamento

---

## 🔐 Segurança (Próximos Passos)

- [ ] Autenticação JWT
- [ ] Validação de permissões
- [ ] Rate limiting
- [ ] CORS restritivo
- [ ] SQL Injection prevention (já feito com SQLAlchemy ORM)

---

## 📚 Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
