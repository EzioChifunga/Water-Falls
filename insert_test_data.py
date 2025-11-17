#!/usr/bin/env python
"""Insert test data (address, category and store) to test vehicle creation"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.infrastructure.config.database import DATABASE_URL
from app.infrastructure.models.endereco_model import EnderecoModel
from app.infrastructure.models.categoria_veiculo_model import CategoriaVeiculoModel
from app.infrastructure.models.loja_model import LojaModel

engine = create_engine(DATABASE_URL, echo=False)

with Session(engine) as session:
    # Create an address
    endereco = EnderecoModel(
        rua="Av. Principal, 100",
        cidade="São Paulo",
        estado="SP"
    )
    session.add(endereco)
    session.flush()
    endereco_id = endereco.id
    print(f"✓ Endereço criado: {endereco_id}")
    
    # Create a category
    categoria = CategoriaVeiculoModel(
        nome="Economia"
    )
    session.add(categoria)
    session.flush()
    categoria_id = categoria.id
    print(f"✓ Categoria criada: {categoria_id}")
    
    # Create a store
    loja = LojaModel(
        nome="Loja Centro",
        telefone="(11) 9999-9999",
        endereco_id=endereco_id
    )
    session.add(loja)
    session.flush()
    loja_id = loja.id
    print(f"✓ Loja criada: {loja_id}")
    
    session.commit()

print(f"\nUse estes IDs na sua requisição POST /veiculos:")
print(f"  categoria_id: {categoria_id}")
print(f"  loja_id: {loja_id}")
