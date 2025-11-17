"""
Serviço de aplicação para gerenciar Clientes
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.clientes import Cliente, Endereco
from app.infrastructure.repositories.cliente_repository import ClienteRepository
from app.infrastructure.repositories.endereco_repository import EnderecoRepository


class ClienteService:
    """Serviço de aplicação para operações com clientes"""
    
    def __init__(self, db: Session):
        self.cliente_repo = ClienteRepository(db)
        self.endereco_repo = EnderecoRepository(db)
    
    def create_cliente(self, nome: str, cpf: str, cnh_numero: str, cnh_validade: str, 
                      telefone: Optional[str] = None, email: Optional[str] = None, 
                      endereco_id: Optional[str] = None) -> Cliente:
        """Criar um novo cliente"""
        
        # Validações de negócio
        existing_cpf = self.cliente_repo.get_by_cpf(cpf)
        if existing_cpf:
            raise ValueError(f"Já existe um cliente com o CPF {cpf}")
        
        if email:
            existing_email = self.cliente_repo.get_by_email(email)
            if existing_email:
                raise ValueError(f"Já existe um cliente com o email {email}")
        
        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            endereco_id=endereco_id,
            cnh_numero=cnh_numero,
            cnh_validade=cnh_validade,
        )
        
        return self.cliente_repo.create(cliente)
    
    def get_cliente(self, cliente_id: str) -> Optional[Cliente]:
        """Obter um cliente pelo ID"""
        return self.cliente_repo.get_by_id(cliente_id)
    
    def get_all_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Obter todos os clientes"""
        return self.cliente_repo.get_all(skip=skip, limit=limit)
    
    def update_cliente(self, cliente_id: str, nome: str, cpf: str, cnh_numero: str, 
                       cnh_validade: str, telefone: Optional[str] = None, 
                       email: Optional[str] = None, endereco_id: Optional[str] = None) -> Optional[Cliente]:
        """Atualizar um cliente"""
        
        existing = self.cliente_repo.get_by_id(cliente_id)
        if not existing:
            return None
        
        # Validar mudanças de email e CPF
        if email and email != existing.email:
            existing_email = self.cliente_repo.get_by_email(email)
            if existing_email:
                raise ValueError(f"Já existe outro cliente com o email {email}")
        
        if cpf != existing.cpf:
            existing_cpf = self.cliente_repo.get_by_cpf(cpf)
            if existing_cpf:
                raise ValueError(f"Já existe outro cliente com o CPF {cpf}")
        
        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            endereco_id=endereco_id,
            cnh_numero=cnh_numero,
            cnh_validade=cnh_validade,
        )
        
        return self.cliente_repo.update(cliente_id, cliente)
    
    def delete_cliente(self, cliente_id: str) -> bool:
        """Deletar um cliente"""
        return self.cliente_repo.delete(cliente_id)
