"""
Modelo ORM para Estoque de Veículos
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.config.database import Base

class EstoqueVeiculoModel(Base):
    """Tabela intermediária para controlar quantidade de veículos por loja"""
    __tablename__ = "estoque_veiculos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    veiculo_id = Column(UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False)
    loja_id = Column(UUID(as_uuid=True), ForeignKey("lojas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    status = Column(Enum('DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA', 'EM_USO', name='status_veiculo'), nullable=False, default='DISPONIVEL')
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<EstoqueVeiculoModel(id={self.id}, veiculo_id={self.veiculo_id}, loja_id={self.loja_id}, quantidade={self.quantidade}, status={self.status})>"
