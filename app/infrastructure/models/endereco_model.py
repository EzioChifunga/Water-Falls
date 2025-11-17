"""
Modelo ORM para Endereços
"""
from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.config.database import Base


class EnderecoModel(Base):
    """Modelo de banco de dados para Endereço"""
    
    __tablename__ = "enderecos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    rua = Column(String(120), nullable=False)
    cidade = Column(String(80), nullable=False)
    estado = Column(String(2), nullable=False)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    
    def __repr__(self):
        return f"<EnderecoModel(id={self.id}, cidade='{self.cidade}')>"
