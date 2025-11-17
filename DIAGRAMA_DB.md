# Diagrama de Relacionamento - WaterFalls API

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────┐         ┌──────────────────────┐
│   enderecos     │         │   categorias_veiculos│
├─────────────────┤         ├──────────────────────┤
│ id (UUID) [PK]  │         │ id (UUID) [PK]       │
│ rua (VARCHAR)   │         │ nome (VARCHAR UNIQUE)│
│ cidade          │         └──────────────────────┘
│ estado          │                    ▲
│ latitude        │                    │
│ longitude       │                    │ FK
└─────────────────┘                    │
        ▲                              │
        │ FK                    ┌──────────────────┐
        │                       │    veiculos      │
    ┌───┴────────────┬──────────┼──────────────────┤
    │                │          │ id (UUID) [PK]   │
    │                │          │ placa (CHAR(7))  │
┌───┴────────┐  ┌────┴──────┐  │ marca (VARCHAR)  │
│  clientes  │  │   lojas   │  │ modelo (VARCHAR) │
├────────────┤  ├───────────┤  │ ano (SMALLINT)   │
│id(UUID)[PK]│  │id(UUID)[PK]  │ categoria_id(FK) │──┐
│nome        │  │nome       │  │ diaria (NUMERIC) │  │ references categorias_veiculos
│cpf(UNIQUE) │  │telefone   │  │ status (ENUM)    │  │
│telefone    │  │endereco_id│─┤ loja_id (FK)     │◄─┤
│email(UNIQUE)   │  │ FK        │  │ latitude/long    │  │ references lojas
│endereco_id │──┘   └──────────┤ criado_em        │
│ (FK)       │      references  │ atualizado_em    │
│cnh_numero  │      enderecos   └──────────────────┘
│cnh_validade│                         ▲
│criado_em   │                         │ FK
│atualizado_em                         │
└────────────┘          ┌──────────────┴────────────────┐
        ▲               │                               │
        │ FK            │                               │
        │         ┌─────┴──────────────┐       ┌────────┴───────────┐
        │         │    reservas        │       │ historico_status   │
        │         ├────────────────────┤       │ _veiculo           │
        │         │ id (UUID) [PK]     │       ├────────────────────┤
        ├─────────┼─ cliente_id (FK)   │       │ id (UUID) [PK]     │
        │         │ veiculo_id (FK)    │───────┤ veiculo_id (FK)    │
        │         │ loja_retirada_id   │       │ status_anterior    │
        │         │ (FK → lojas)       │       │ status_atual       │
        │         │ loja_devolucao_id  │       │ data_mudanca       │
        │         │ (FK → lojas)       │       └────────────────────┘
        │         │ data_inicio        │
        │         │ data_fim           │
        │         │ periodo            │
        │         │ valor_total        │
        │         │ motorista_incluido │
        │         │ canal_origem       │
        │         │ status             │
        │         │ criado_em          │
        │         │ atualizado_em      │
        │         └────────────┬───────┘
        │                      │ FK
        │                      │
        │              ┌───────┴──────────┐
        │              │   pagamentos     │
        │              ├──────────────────┤
        │              │ id (UUID) [PK]   │
        │              │ reserva_id (FK)  │
        └──────────────┤ UNIQUE           │
                       │ metodo (ENUM)    │
                       │ status (ENUM)    │
                       │ valor (NUMERIC)  │
                       │ transacao_gateway│
                       │ criado_em        │
                       └──────────────────┘
```

---

## 🔗 Relacionamentos Principais

### 1. Cliente → Endereço (opcional)
- Um cliente pode ter **1** endereço
- Um endereço pode pertencer a **múltiplos** clientes ou lojas
- Tipo: **Many-to-One** (opcional)

### 2. Loja → Endereço (obrigatório)
- Uma loja deve ter **1** endereço
- Tipo: **Many-to-One** (obrigatório)

### 3. Veículo → Loja
- Um veículo pertence a **1** loja
- Uma loja pode ter **múltiplos** veículos
- Tipo: **Many-to-One**

### 4. Veículo → Categoria
- Um veículo tem **1** categoria
- Uma categoria pode ter **múltiplos** veículos
- Tipo: **Many-to-One**

### 5. Reserva → Cliente
- Uma reserva é feita por **1** cliente
- Um cliente pode ter **múltiplas** reservas
- Tipo: **Many-to-One**

### 6. Reserva → Veículo
- Uma reserva é para **1** veículo
- Um veículo pode ter **múltiplas** reservas
- Tipo: **Many-to-One**

### 7. Reserva → Loja (Retirada/Devolução)
- Uma reserva tem retirada em **1** loja
- Uma reserva tem devolução em **1** loja (pode ser diferente)
- Tipo: **Many-to-One** (2x)

### 8. Pagamento → Reserva
- Um pagamento é vinculado a **1** reserva (UNIQUE)
- Uma reserva deve ter **1** pagamento
- Tipo: **One-to-One**

### 9. Histórico Status → Veículo
- Um histórico pertence a **1** veículo
- Um veículo pode ter **múltiplos** registros de histórico
- Tipo: **Many-to-One** (auditoria)

---

## 📋 Chaves Primárias e Estrangeiras

| Tabela | PK | FK | Descrição |
|--------|----|----|-----------|
| enderecos | id | - | Base de dados de localizações |
| clientes | id | endereco_id | Referencia endereço (opcional) |
| lojas | id | endereco_id | Referencia endereço (obrigatório) |
| categorias_veiculos | id | - | Tipos de veículos |
| veiculos | id | categoria_id, loja_id | Referencia categoria e loja |
| reservas | id | cliente_id, veiculo_id, loja_retirada_id, loja_devolucao_id | Referencia 4 tabelas |
| pagamentos | id | reserva_id | Referencia reserva (UNIQUE) |
| historico_status_veiculo | id | veiculo_id | Rastreia mudanças de status |

---

## 🔄 Fluxo de Uma Reserva (Use Case)

```
1. Cliente solicita reserva
   ↓
   ├─ Valida cliente (existe e CNH válida?)
   ├─ Valida veículo (existe e disponível?)
   └─ Valida período (7, 15 ou 30 dias)
   ↓
2. Cria RESERVA com status: PENDENTE_PAGAMENTO
   ├─ Muda status do veículo para: RESERVADO
   └─ Relaciona lojas de retirada/devolução
   ↓
3. Cliente realiza PAGAMENTO
   ├─ Cria registro de PAGAMENTO (PENDENTE)
   └─ Processa gateway de pagamento
   ↓
4. Se pagamento CONFIRMADO
   ├─ RESERVA status → CONFIRMADA
   ├─ Veículo status → ALUGADO
   └─ Registra histórico de mudança
   ↓
5. Cliente retira o veículo
   ├─ RESERVA status → EM_CURSO
   └─ Atualiza localização (lat/lon)
   ↓
6. Cliente devolve o veículo
   ├─ RESERVA status → FINALIZADA
   ├─ Veículo status → DISPONIVEL
   └─ Registra histórico final
```

---

## 💾 Constraints Aplicados

### CHECK Constraints
- `reservas.periodo IN (7, 15, 30)` - Apenas períodos válidos
- `pagamentos.status IN ('PAGO', 'PENDENTE', 'RECUSADO')`
- `veiculos.status IN ('DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA')`

### UNIQUE Constraints
- `clientes.cpf` - CPF único por cliente
- `clientes.email` - Email único por cliente
- `clientes.cnh_numero` - CNH única
- `veiculos.placa` - Placa única
- `categorias_veiculos.nome` - Categoria única
- `pagamentos.reserva_id` - 1 pagamento por reserva
- `pagamentos.transacao_gateway_id` - Transação única

### NOT NULL Constraints
- Todos os campos obrigatórios marcados como NOT NULL no SQL

---

## 📊 Índices

Automaticamente criados em:
- Chaves primárias (UUID)
- Chaves estrangeiras
- Campos UNIQUE
- Campos frequentemente buscados (cpf, email, placa, cnh_numero)

---

## 🎯 Cardinalidade Resumida

```
Endereço:
  ├─ 0..* Clientes (Many-to-One Opcional)
  └─ 1..* Lojas (Many-to-One Obrigatório)

Categoria Veículo:
  └─ 1..* Veículos

Loja:
  └─ 1..* Veículos
  └─ 1..* Reservas (retirada e devolução)

Veículo:
  ├─ 1 Loja
  ├─ 1 Categoria
  ├─ 1..* Reservas
  └─ 0..* Histórico Status

Cliente:
  ├─ 0..1 Endereço (opcional)
  └─ 0..* Reservas

Reserva:
  ├─ 1 Cliente
  ├─ 1 Veículo
  ├─ 1 Loja (retirada)
  ├─ 1 Loja (devolucao)
  └─ 1 Pagamento (One-to-One)

Pagamento:
  └─ 1 Reserva
```
