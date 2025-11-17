"""
Repositório para operações com Clientes
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.clientes import Cliente
from app.infrastructure.models.cliente_model import ClienteModel


class ClienteRepository:
    """Repositório para gerenciar clientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, cliente: Cliente) -> Cliente:
        """Cria um novo cliente"""
        db_cliente = ClienteModel(
            nome=cliente.nome,
            cpf=cliente.cpf,
            telefone=cliente.telefone,
            email=cliente.email,
            endereco_id=cliente.endereco_id,
            cnh_numero=cliente.cnh_numero,
            cnh_validade=cliente.cnh_validade,
        )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return self._to_domain(db_cliente)
    
    def get_by_id(self, cliente_id: str) -> Optional[Cliente]:
        """Obtém um cliente pelo ID"""
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
        return self._to_domain(db_cliente) if db_cliente else None
    
    def get_by_cpf(self, cpf: str) -> Optional[Cliente]:
        """Obtém um cliente pelo CPF"""
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()
        return self._to_domain(db_cliente) if db_cliente else None
    
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Obtém um cliente pelo email"""
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.email == email).first()
        return self._to_domain(db_cliente) if db_cliente else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Obtém todos os clientes"""
        db_clientes = self.db.query(ClienteModel).offset(skip).limit(limit).all()
        return [self._to_domain(c) for c in db_clientes]
    
    def update(self, cliente_id: str, cliente: Cliente) -> Optional[Cliente]:
        """Atualiza um cliente"""
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
        if not db_cliente:
            return None
        
        db_cliente.nome = cliente.nome
        db_cliente.cpf = cliente.cpf
        db_cliente.telefone = cliente.telefone
        db_cliente.email = cliente.email
        db_cliente.endereco_id = cliente.endereco_id
        db_cliente.cnh_numero = cliente.cnh_numero
        db_cliente.cnh_validade = cliente.cnh_validade
        
        self.db.commit()
        self.db.refresh(db_cliente)
        return self._to_domain(db_cliente)
    
    def delete(self, cliente_id: str) -> bool:
        """Deleta um cliente"""
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
        if not db_cliente:
            return False
        
        self.db.delete(db_cliente)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_cliente: ClienteModel) -> Cliente:
        """Converte modelo ORM para entidade de domínio"""
        return Cliente(
            id=str(db_cliente.id),
            nome=db_cliente.nome,
            cpf=db_cliente.cpf,
            telefone=db_cliente.telefone,
            email=db_cliente.email,
            endereco_id=str(db_cliente.endereco_id) if db_cliente.endereco_id else None,
            cnh_numero=db_cliente.cnh_numero,
            cnh_validade=str(db_cliente.cnh_validade) if db_cliente.cnh_validade else None,
            criado_em=db_cliente.criado_em,
            atualizado_em=db_cliente.atualizado_em,
        )
