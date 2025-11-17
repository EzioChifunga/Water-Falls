# 🚀 WaterFalls API - Início Rápido

## 3 Passos para Começar

### Passo 1: Preparar Ambiente
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Passo 2: Configurar Banco de Dados
Crie arquivo `.env`:
```
DATABASE_URL=postgresql://postgres:asdadsdad6s56adsa@31.97.170.13:5433/water_falls?sslmode=disable
```

### Passo 3: Iniciar
```powershell
python main.py
```

✅ Pronto! Acesse http://127.0.0.1:8000/docs

---

## 10 Exemplos Práticos

### 1. Criar um Endereço
```bash
curl -X POST http://127.0.0.1:8000/enderecos/ \
  -H "Content-Type: application/json" \
  -d '{"rua":"Av Paulista","cidade":"São Paulo","estado":"SP","latitude":-23.55,"longitude":-46.63}'
```

### 2. Criar uma Loja
```bash
curl -X POST http://127.0.0.1:8000/lojas/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Loja Centro","telefone":"1133334444","endereco_id":"PASTE_ENDERECO_ID_AQUI"}'
```

### 3. Criar Categoria de Veículo
```bash
curl -X POST http://127.0.0.1:8000/categorias/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"SUV"}'
```

### 4. Criar um Veículo
```bash
curl -X POST http://127.0.0.1:8000/veiculos/ \
  -H "Content-Type: application/json" \
  -d '{
    "placa":"ABC1234",
    "marca":"Toyota",
    "modelo":"Corolla",
    "ano":2023,
    "cor":"Branco",
    "combustivel":"Flex",
    "portas":4,
    "cambio":"Automático",
    "quilometragem":5000,
    "categoria_id":"PASTE_CATEGORIA_ID",
    "diaria":150,
    "status":"DISPONIVEL",
    "loja_id":"PASTE_LOJA_ID",
    "latitude":-23.55,
    "longitude":-46.63
  }'
```

### 5. Criar um Cliente
```bash
curl -X POST http://127.0.0.1:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome":"João Silva",
    "cpf":"12345678901",
    "telefone":"1199999999",
    "email":"joao@example.com",
    "endereco_id":"PASTE_ENDERECO_ID",
    "cnh_numero":"123456789",
    "cnh_validade":"2030-12-31"
  }'
```

### 6. Criar uma Reserva
```bash
curl -X POST http://127.0.0.1:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id":"PASTE_CLIENTE_ID",
    "veiculo_id":"PASTE_VEICULO_ID",
    "loja_retirada_id":"PASTE_LOJA_ID",
    "loja_devolucao_id":"PASTE_LOJA_ID",
    "data_inicio":"2024-12-01",
    "data_fim":"2024-12-08",
    "periodo":7,
    "valor_total":1050,
    "motorista_incluido":false,
    "canal_origem":"WEB",
    "status":"CONFIRMADA"
  }'
```

### 7. Criar um Pagamento
```bash
curl -X POST http://127.0.0.1:8000/pagamentos/ \
  -H "Content-Type: application/json" \
  -d '{
    "reserva_id":"PASTE_RESERVA_ID",
    "metodo":"CARTAO",
    "status":"PENDENTE",
    "valor":1050,
    "transacao_gateway_id":"TRX123456"
  }'
```

### 8. Listar Todos os Endereços
```bash
curl -X GET http://127.0.0.1:8000/enderecos/
```

### 9. Atualizar um Endereço
```bash
curl -X PUT http://127.0.0.1:8000/enderecos/PASTE_ID \
  -H "Content-Type: application/json" \
  -d '{"rua":"Rua Nova","cidade":"São Paulo","estado":"SP"}'
```

### 10. Deletar um Endereço
```bash
curl -X DELETE http://127.0.0.1:8000/enderecos/PASTE_ID
```

---

## 📚 Documentação Completa

Para documentação detalhada, veja `API_GUIDE.md`

## 🆘 Precisa de Ajuda?

1. **Documentação Interativa**: http://127.0.0.1:8000/docs
2. **ReDoc**: http://127.0.0.1:8000/redoc
3. **Arquivo API_GUIDE.md** com todos os endpoints

---

## Estrutura Base de Dados

```sql
Tabelas criadas:
- enderecos
- lojas
- categorias_veiculos
- veiculos
- clientes
- reservas
- pagamentos
- historico_status_veiculo
- cars (legado)
```

Todas as tabelas já foram criadas via Alembic migrations. ✅
