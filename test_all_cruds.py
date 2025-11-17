"""
Script de teste completo para todos os CRUDs
"""
import requests
import json
from uuid import uuid4
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_endereco():
    """Testa endpoints de Endereço"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD ENDEREÇO ===")
    print("="*80)
    
    # CREATE
    endereco_data = {
        "rua": "Rua das Flores",
        "cidade": "São Paulo",
        "estado": "SP",
        "latitude": -23.55,
        "longitude": -46.63
    }
    response = requests.post(f"{BASE_URL}/enderecos/", json=endereco_data)
    print(f"\n✓ POST /enderecos/: {response.status_code}")
    if response.status_code == 201:
        endereco = response.json()
        endereco_id = endereco["id"]
        print(f"  ID: {endereco_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/enderecos/{endereco_id}")
        print(f"✓ GET /enderecos/{endereco_id[:8]}...: {response.status_code}")
        
        # UPDATE
        update_data = {
            "rua": "Rua das Árvores",
            "cidade": "São Paulo",
            "estado": "SP",
        }
        response = requests.put(f"{BASE_URL}/enderecos/{endereco_id}", json=update_data)
        print(f"✓ PUT /enderecos/{endereco_id[:8]}...: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/enderecos/")
        print(f"✓ GET /enderecos/: {response.status_code} - {len(response.json())} registros")
        
        # NÃO DELETAR - será usado por Loja e Cliente
        return endereco_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def test_cliente(endereco_id):
    """Testa endpoints de Cliente"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD CLIENTE ===")
    print("="*80)
    
    if not endereco_id:
        print("✗ Endereço necessário para criar Cliente")
        return None
    
    # CREATE
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "telefone": "1199999999",
        "email": "joao@example.com",
        "endereco_id": endereco_id,
        "cnh_numero": "123456789",
        "cnh_validade": "2030-12-31"
    }
    response = requests.post(f"{BASE_URL}/clientes/", json=cliente_data)
    print(f"\n✓ POST /clientes/: {response.status_code}")
    if response.status_code == 201:
        cliente = response.json()
        cliente_id = cliente["id"]
        print(f"  ID: {cliente_id}")
        return cliente_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def test_categoria():
    """Testa endpoints de Categoria"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD CATEGORIA VEÍCULO ===")
    print("="*80)
    
    # CREATE
    categoria_data = {"nome": "SUV"}
    response = requests.post(f"{BASE_URL}/categorias/", json=categoria_data)
    print(f"\n✓ POST /categorias/: {response.status_code}")
    if response.status_code == 201:
        categoria = response.json()
        categoria_id = categoria["id"]
        print(f"  ID: {categoria_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/categorias/{categoria_id}")
        print(f"✓ GET /categorias/{categoria_id[:8]}...: {response.status_code}")
        
        # UPDATE
        update_data = {"nome": "SUV Premium"}
        response = requests.put(f"{BASE_URL}/categorias/{categoria_id}", json=update_data)
        print(f"✓ PUT /categorias/{categoria_id[:8]}...: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/categorias/")
        print(f"✓ GET /categorias/: {response.status_code} - {len(response.json())} registros")
        
        # NÃO DELETAR - será usado por Veículo
        return categoria_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def test_loja(endereco_id):
    """Testa endpoints de Loja"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD LOJA ===")
    print("="*80)
    
    if not endereco_id:
        print("✗ Endereço necessário para criar Loja")
        return None
    
    # CREATE
    loja_data = {
        "nome": "Loja Centro",
        "telefone": "1133334444",
        "endereco_id": endereco_id
    }
    response = requests.post(f"{BASE_URL}/lojas/", json=loja_data)
    print(f"\n✓ POST /lojas/: {response.status_code}")
    if response.status_code == 201:
        loja = response.json()
        loja_id = loja["id"]
        print(f"  ID: {loja_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/lojas/{loja_id}")
        print(f"✓ GET /lojas/{loja_id[:8]}...: {response.status_code}")
        
        # UPDATE
        update_data = {
            "nome": "Loja Centro Premium",
            "telefone": "1133334444",
            "endereco_id": endereco_id
        }
        response = requests.put(f"{BASE_URL}/lojas/{loja_id}", json=update_data)
        print(f"✓ PUT /lojas/{loja_id[:8]}...: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/lojas/")
        print(f"✓ GET /lojas/: {response.status_code} - {len(response.json())} registros")
        
        return loja_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def test_veiculo(categoria_id, loja_id):
    """Testa endpoints de Veículo"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD VEÍCULO ===")
    print("="*80)
    
    if not categoria_id or not loja_id:
        print("✗ Categoria e Loja necessárias para criar Veículo")
        return None
    
    # CREATE
    veiculo_data = {
        "placa": "ABC1234",
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2023,
        "cor": "Branco",
        "combustivel": "Flex",
        "portas": 4,
        "cambio": "Automático",
        "quilometragem": 5000.0,
        "categoria_id": categoria_id,
        "diaria": 150.0,
        "status": "DISPONIVEL",
        "loja_id": loja_id,
        "latitude": -23.55,
        "longitude": -46.63
    }
    response = requests.post(f"{BASE_URL}/veiculos/", json=veiculo_data)
    print(f"\n✓ POST /veiculos/: {response.status_code}")
    if response.status_code == 201:
        veiculo = response.json()
        veiculo_id = veiculo["id"]
        print(f"  ID: {veiculo_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/veiculos/{veiculo_id}")
        print(f"✓ GET /veiculos/{veiculo_id[:8]}...: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/veiculos/")
        print(f"✓ GET /veiculos/: {response.status_code} - {len(response.json())} registros")
        
        return veiculo_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def test_historico(veiculo_id):
    """Testa endpoints de Histórico"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD HISTÓRICO DE STATUS VEÍCULO ===")
    print("="*80)
    
    if not veiculo_id:
        print("✗ Veículo necessário para criar Histórico")
        return
    
    # CREATE
    historico_data = {
        "veiculo_id": veiculo_id,
        "status_anterior": "DISPONIVEL",
        "status_atual": "ALUGADO"
    }
    response = requests.post(f"{BASE_URL}/historico-status-veiculo/", json=historico_data)
    print(f"\n✓ POST /historico-status-veiculo/: {response.status_code}")
    if response.status_code == 201:
        historico = response.json()
        historico_id = historico["id"]
        print(f"  ID: {historico_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/{historico_id}")
        print(f"✓ GET /historico-status-veiculo/{historico_id[:8]}...: {response.status_code}")
        
        # GET by VEICULO
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/veiculo/{veiculo_id}")
        print(f"✓ GET /historico-status-veiculo/veiculo/{veiculo_id[:8]}...: {response.status_code} - {len(response.json())} registros")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/")
        print(f"✓ GET /historico-status-veiculo/: {response.status_code} - {len(response.json())} registros")
    else:
        print(f"✗ Erro: {response.text}")


def test_pagamento(veiculo_id, cliente_id, loja_id):
    """Testa endpoints de Pagamento"""
    print("\n" + "="*80)
    print("=== TESTANDO CRUD PAGAMENTO ===")
    print("="*80)
    
    if not veiculo_id or not cliente_id or not loja_id:
        print("✗ Veículo, Cliente e Loja necessários para criar Reserva e Pagamento")
        return
    
    # Primeiro, criar uma Reserva
    from datetime import date, timedelta
    hoje = date.today()
    amanha = hoje + timedelta(days=1)
    
    reserva_data = {
        "cliente_id": cliente_id,
        "veiculo_id": veiculo_id,
        "loja_retirada_id": loja_id,
        "loja_devolucao_id": loja_id,
        "data_inicio": hoje.isoformat(),
        "data_fim": amanha.isoformat(),
        "periodo": 7,
        "valor_total": 500.0,
        "motorista_incluido": False,
        "canal_origem": "WEB",
        "status": "CONFIRMADA"
    }
    response = requests.post(f"{BASE_URL}/reservas/", json=reserva_data)
    if response.status_code != 201:
        print(f"✗ Erro ao criar reserva para pagamento: {response.text}")
        return
    
    reserva = response.json()
    reserva_id = reserva["id"]
    
    # CREATE Pagamento
    pagamento_data = {
        "reserva_id": reserva_id,
        "metodo": "CARTAO",
        "status": "PENDENTE",
        "valor": 500.0,
        "transacao_gateway_id": "TRX123456"
    }
    response = requests.post(f"{BASE_URL}/pagamentos/", json=pagamento_data)
    print(f"\n✓ POST /pagamentos/: {response.status_code}")
    if response.status_code == 201:
        pagamento = response.json()
        pagamento_id = pagamento["id"]
        print(f"  ID: {pagamento_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/pagamentos/{pagamento_id}")
        print(f"✓ GET /pagamentos/{pagamento_id[:8]}...: {response.status_code}")
        
        # UPDATE
        update_data = {
            "metodo": "CARTAO",
            "status": "PAGO",
            "valor": 500.0,
        }
        response = requests.put(f"{BASE_URL}/pagamentos/{pagamento_id}", json=update_data)
        print(f"✓ PUT /pagamentos/{pagamento_id[:8]}...: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/pagamentos/")
        print(f"✓ GET /pagamentos/: {response.status_code} - {len(response.json())} registros")
        
        # GET by STATUS
        response = requests.get(f"{BASE_URL}/pagamentos/?status=PAGO")
        print(f"✓ GET /pagamentos/?status=PAGO: {response.status_code} - {len(response.json())} registros")
    else:
        print(f"✗ Erro: {response.text}")


if __name__ == "__main__":
    try:
        print("\n" + "#"*80)
        print("# TESTE COMPLETO DO WATERFALLS API")
        print("#"*80)
        
        endereco_id = test_endereco()
        categoria_id = test_categoria()
        loja_id = test_loja(endereco_id)
        cliente_id = test_cliente(endereco_id)
        veiculo_id = test_veiculo(categoria_id, loja_id)
        test_historico(veiculo_id)
        test_pagamento(veiculo_id, cliente_id, loja_id)
        
        print("\n" + "#"*80)
        print("# ✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("#"*80 + "\n")
    except Exception as e:
        print(f"\n✗ Erro geral: {e}")
        import traceback
        traceback.print_exc()
