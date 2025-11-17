"""
Modelo ORM para Histórico de Status de Veículo
"""
from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from app.infrastructure.config.database import Base


class HistoricoStatusVeiculoModel(Base):
    """Modelo de banco de dados para Histórico de Status de Veículo"""
    
    __tablename__ = "historico_status_veiculo"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    veiculo_id = Column(UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True)
    status_anterior = Column(
        ENUM('DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA', name='status_veiculo'),
        nullable=True
    )
    status_atual = Column(
        ENUM('DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA', name='status_veiculo'),
        nullable=False
    )
    data_mudanca = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<HistoricoStatusVeiculoModel(id={self.id}, veiculo_id={self.veiculo_id}, status='{self.status_atual}')>"
