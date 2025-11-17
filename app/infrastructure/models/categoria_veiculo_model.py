"""
Modelo ORM para Categorias de Veículos
"""
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.config.database import Base


class CategoriaVeiculoModel(Base):
    """Modelo de banco de dados para Categoria de Veículo"""
    
    __tablename__ = "categorias_veiculos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(60), unique=True, nullable=False, index=True)
    
    def __repr__(self):
        return f"<CategoriaVeiculoModel(id={self.id}, nome='{self.nome}')>"
