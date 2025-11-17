"""
Modelo ORM para Veículos
"""
from sqlalchemy import Column, String, SmallInteger, Numeric, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from app.infrastructure.config.database import Base


class VeiculoModel(Base):
    """Modelo de banco de dados para Veículo"""
    
    __tablename__ = "veiculos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    placa = Column(String(7), unique=True, nullable=False, index=True)
    marca = Column(String(60), nullable=False)
    modelo = Column(String(60), nullable=False)
    ano = Column(SmallInteger, nullable=False)
    cor = Column(String(30), nullable=True)
    combustivel = Column(String(30), nullable=True)
    portas = Column(SmallInteger, nullable=True)
    cambio = Column(String(30), nullable=True)
    quilometragem = Column(Numeric(12, 2), nullable=True)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias_veiculos.id"), nullable=False)
    diaria = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(255), nullable=True)
    status = Column(
        ENUM('DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA', 'EM_USO', name='status_veiculo'),
        nullable=False,
        default='DISPONIVEL'
    )
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return (
            f"<VeiculoModel(id={self.id}, placa='{self.placa}', marca='{self.marca}', "
            f"modelo='{self.modelo}', cor='{self.cor}', status='{self.status}')>"
        )
