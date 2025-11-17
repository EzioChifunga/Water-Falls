"""
Modelo ORM para Clientes
"""
from sqlalchemy import Column, String, Date, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.config.database import Base


class ClienteModel(Base):
    """Modelo de banco de dados para Cliente"""
    
    __tablename__ = "clientes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(120), unique=True, nullable=True, index=True)
    endereco_id = Column(UUID(as_uuid=True), ForeignKey("enderecos.id"), nullable=True)
    cnh_numero = Column(String(20), nullable=False, unique=True)
    cnh_validade = Column(Date, nullable=False)
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<ClienteModel(id={self.id}, nome='{self.nome}', cpf='{self.cpf}')>"
