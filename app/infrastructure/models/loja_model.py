"""
Modelo ORM para Lojas
"""
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.config.database import Base


class LojaModel(Base):
    """Modelo de banco de dados para Loja"""
    
    __tablename__ = "lojas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(120), nullable=False)
    telefone = Column(String(20), nullable=True)
    endereco_id = Column(UUID(as_uuid=True), ForeignKey("enderecos.id"), nullable=False)
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<LojaModel(id={self.id}, nome='{self.nome}')>"
