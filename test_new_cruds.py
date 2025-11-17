"""
Script de teste para os novos CRUDs: Endereco, Pagamento, HistoricoStatusVeiculo
"""
import requests
import json
from uuid import uuid4

BASE_URL = "http://127.0.0.1:8000"

def test_endereco():
    """Testa endpoints de Endereço"""
    print("\n=== Testando CRUD Endereço ===")
    
    # CREATE
    endereco_data = {
        "rua": "Rua das Flores",
        "cidade": "São Paulo",
        "estado": "SP",
        "latitude": -23.55,
        "longitude": -46.63
    }
    response = requests.post(f"{BASE_URL}/enderecos/", json=endereco_data)
    print(f"POST /enderecos/: {response.status_code}")
    if response.status_code == 201:
        endereco = response.json()
        endereco_id = endereco["id"]
        print(f"✓ Endereço criado: {endereco_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/enderecos/{endereco_id}")
        print(f"GET /enderecos/{endereco_id}: {response.status_code}")
        
        # UPDATE
        update_data = {
            "rua": "Rua das Árvores",
            "cidade": "São Paulo",
            "estado": "SP",
            "latitude": -23.55,
            "longitude": -46.63
        }
        response = requests.put(f"{BASE_URL}/enderecos/{endereco_id}", json=update_data)
        print(f"PUT /enderecos/{endereco_id}: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/enderecos/")
        print(f"GET /enderecos/: {response.status_code} - {len(response.json())} registros")
        
        # DELETE
        response = requests.delete(f"{BASE_URL}/enderecos/{endereco_id}")
        print(f"DELETE /enderecos/{endereco_id}: {response.status_code}")
    else:
        print(f"✗ Erro ao criar endereço: {response.text}")


def test_pagamento():
    """Testa endpoints de Pagamento"""
    print("\n=== Testando CRUD Pagamento ===")
    
    # Criar uma reserva fake para usar como foreign key
    reserva_id = str(uuid4())
    
    # CREATE
    pagamento_data = {
        "reserva_id": reserva_id,
        "metodo": "CARTAO",
        "status": "PENDENTE",
        "valor": 500.00,
        "transacao_gateway_id": "TRX123456"
    }
    response = requests.post(f"{BASE_URL}/pagamentos/", json=pagamento_data)
    print(f"POST /pagamentos/: {response.status_code}")
    if response.status_code == 201:
        pagamento = response.json()
        pagamento_id = pagamento["id"]
        print(f"✓ Pagamento criado: {pagamento_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/pagamentos/{pagamento_id}")
        print(f"GET /pagamentos/{pagamento_id}: {response.status_code}")
        
        # UPDATE
        update_data = {
            "metodo": "CARTAO",
            "status": "PAGO",
            "valor": 500.00,
            "transacao_gateway_id": "TRX123456"
        }
        response = requests.put(f"{BASE_URL}/pagamentos/{pagamento_id}", json=update_data)
        print(f"PUT /pagamentos/{pagamento_id}: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/pagamentos/")
        print(f"GET /pagamentos/: {response.status_code} - {len(response.json())} registros")
        
        # GET by STATUS
        response = requests.get(f"{BASE_URL}/pagamentos/?status=PAGO")
        print(f"GET /pagamentos/?status=PAGO: {response.status_code}")
        
        # DELETE
        response = requests.delete(f"{BASE_URL}/pagamentos/{pagamento_id}")
        print(f"DELETE /pagamentos/{pagamento_id}: {response.status_code}")
    else:
        print(f"✗ Erro ao criar pagamento: {response.text}")


def test_historico():
    """Testa endpoints de Histórico de Status de Veículo"""
    print("\n=== Testando CRUD Histórico de Status de Veículo ===")
    
    # Usar um veiculo_id fake
    veiculo_id = str(uuid4())
    
    # CREATE
    historico_data = {
        "veiculo_id": veiculo_id,
        "status_anterior": "DISPONIVEL",
        "status_atual": "ALUGADO"
    }
    response = requests.post(f"{BASE_URL}/historico-status-veiculo/", json=historico_data)
    print(f"POST /historico-status-veiculo/: {response.status_code}")
    if response.status_code == 201:
        historico = response.json()
        historico_id = historico["id"]
        print(f"✓ Histórico criado: {historico_id}")
        
        # GET by ID
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/{historico_id}")
        print(f"GET /historico-status-veiculo/{historico_id}: {response.status_code}")
        
        # GET by VEICULO
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/veiculo/{veiculo_id}")
        print(f"GET /historico-status-veiculo/veiculo/{veiculo_id}: {response.status_code}")
        
        # GET ALL
        response = requests.get(f"{BASE_URL}/historico-status-veiculo/")
        print(f"GET /historico-status-veiculo/: {response.status_code} - {len(response.json())} registros")
    else:
        print(f"✗ Erro ao criar histórico: {response.text}")


if __name__ == "__main__":
    try:
        test_endereco()
        test_pagamento()
        test_historico()
        print("\n✓ Todos os testes concluídos!")
    except Exception as e:
        print(f"\n✗ Erro geral: {e}")
