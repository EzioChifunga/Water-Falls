# Exemplos de Requisições - WaterFalls API

## 🚀 Testando com cURL ou Postman

### 1️⃣ CARS - Sistema Original

#### Criar um Carro
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

#### Listar Carros
```bash
curl -X GET "http://localhost:8000/cars/?skip=0&limit=10"
```

#### Obter um Carro
```bash
curl -X GET "http://localhost:8000/cars/1"
```

#### Atualizar Carro
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

#### Deletar Carro
```bash
curl -X DELETE "http://localhost:8000/cars/1"
```

---

### 2️⃣ CLIENTES

#### Criar um Cliente
```bash
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "cnh_numero": "1234567890",
    "cnh_validade": "2025-12-31",
    "telefone": "(11) 99999-9999",
    "email": "joao@example.com",
    "endereco_id": null
  }'
```

#### Listar Clientes
```bash
curl -X GET "http://localhost:8000/clientes/?skip=0&limit=10"
```

#### Obter um Cliente
```bash
curl -X GET "http://localhost:8000/clientes/{cliente_id}"
```

#### Atualizar Cliente
```bash
curl -X PUT "http://localhost:8000/clientes/{cliente_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Santos",
    "cpf": "12345678901",
    "cnh_numero": "1234567890",
    "cnh_validade": "2025-12-31",
    "telefone": "(11) 98888-8888",
    "email": "joao@example.com"
  }'
```

#### Deletar Cliente
```bash
curl -X DELETE "http://localhost:8000/clientes/{cliente_id}"
```

---

### 3️⃣ VEÍCULOS

#### Criar um Veículo
```bash
curl -X POST "http://localhost:8000/veiculos/" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "XYZ1234",
    "marca": "Volkswagen",
    "modelo": "Gol",
    "ano": 2023,
    "categoria_id": "{categoria_uuid}",
    "diaria": 150.00,
    "loja_id": "{loja_uuid}",
    "latitude": -23.5505,
    "longitude": -46.6333
  }'
```

#### Listar Veículos
```bash
curl -X GET "http://localhost:8000/veiculos/?skip=0&limit=10"
```

#### Buscar Veículo por Placa
```bash
curl -X GET "http://localhost:8000/veiculos/placa/XYZ1234"
```

#### Obter Veículos Disponíveis
```bash
curl -X GET "http://localhost:8000/veiculos/disponveis?skip=0&limit=10"
```

#### Obter Veículos de uma Loja
```bash
curl -X GET "http://localhost:8000/veiculos/loja/{loja_id}?skip=0&limit=10"
```

#### Atualizar Status do Veículo
```bash
curl -X PATCH "http://localhost:8000/veiculos/{veiculo_id}/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "ALUGADO"
  }'
```

Status válidos: `DISPONIVEL`, `ALUGADO`, `RESERVADO`, `MANUTENCAO`, `FORA_AREA`

---

### 4️⃣ RESERVAS

#### Criar uma Reserva
```bash
curl -X POST "http://localhost:8000/reservas/" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "{cliente_uuid}",
    "veiculo_id": "{veiculo_uuid}",
    "loja_retirada_id": "{loja_uuid}",
    "loja_devolucao_id": "{loja_uuid}",
    "data_inicio": "2025-12-01",
    "data_fim": "2025-12-08",
    "periodo": 7,
    "valor_total": 1050.00,
    "motorista_incluido": true,
    "canal_origem": "WEB"
  }'
```

#### Listar Reservas
```bash
curl -X GET "http://localhost:8000/reservas/?skip=0&limit=10"
```

#### Obter uma Reserva
```bash
curl -X GET "http://localhost:8000/reservas/{reserva_id}"
```

#### Reservas de um Cliente
```bash
curl -X GET "http://localhost:8000/reservas/cliente/{cliente_id}?skip=0&limit=10"
```

#### Reservas de um Veículo
```bash
curl -X GET "http://localhost:8000/reservas/veiculo/{veiculo_id}?skip=0&limit=10"
```

#### Confirmar Reserva
```bash
curl -X PATCH "http://localhost:8000/reservas/{reserva_id}/confirmar"
```

#### Cancelar Reserva
```bash
curl -X PATCH "http://localhost:8000/reservas/{reserva_id}/cancelar"
```

#### Deletar Reserva
```bash
curl -X DELETE "http://localhost:8000/reservas/{reserva_id}"
```

---

## 📊 Respostas Esperadas

### Sucesso (200, 201)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nome": "João Silva",
  "cpf": "12345678901",
  "email": "joao@example.com",
  "telefone": "(11) 99999-9999",
  "cnh_numero": "1234567890",
  "cnh_validade": "2025-12-31"
}
```

### Erro (400)
```json
{
  "detail": "Já existe um carro com a placa ABC1234"
}
```

### Não Encontrado (404)
```json
{
  "detail": "Cliente não encontrado"
}
```

---

## 🧪 Testando com Postman

1. Abra o Postman
2. Crie uma nova Collection: "WaterFalls API"
3. Para cada endpoint:
   - URL: `http://localhost:8000/cars/` (exemplo)
   - Method: POST, GET, PUT, DELETE
   - Headers: `Content-Type: application/json`
   - Body: JSON com dados

---

## 📝 Notas

- Substitua `{cliente_uuid}`, `{veiculo_uuid}` pelos IDs reais retornados
- Período de reserva deve ser: 7, 15 ou 30 dias
- Canal de origem: WEB, LOJA ou TELEFONE
- Todos os timestamps são retornados em ISO 8601 format
