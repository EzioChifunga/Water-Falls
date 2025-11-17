"""
Modelo ORM para Reservas
"""
from sqlalchemy import Column, String, Date, DateTime, func, ForeignKey, Boolean, Numeric, CheckConstraint
from sqlalchemy import Column, String, Date, DateTime, func, ForeignKey, Boolean, Numeric, SmallInteger, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from app.infrastructure.config.database import Base


class ReservaModel(Base):
    """Modelo de banco de dados para Reserva"""
    
    __tablename__ = "reservas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    veiculo_id = Column(UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False)
    loja_retirada_id = Column(UUID(as_uuid=True), ForeignKey("lojas.id"), nullable=False)
    loja_devolucao_id = Column(UUID(as_uuid=True), ForeignKey("lojas.id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    periodo = Column(SmallInteger, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    motorista_incluido = Column(Boolean, default=False, nullable=False)
    canal_origem = Column(
        ENUM('WEB', 'LOJA', 'TELEFONE', name='canal_origem'),
        nullable=False,
        default='WEB'
    )
    status = Column(
        ENUM('PENDENTE_PAGAMENTO', 'CONFIRMADA', 'EM_CURSO', 'FINALIZADA', 'CANCELADA', name='status_reserva'),
        nullable=False,
        default='PENDENTE_PAGAMENTO'
    )
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint("periodo IN (7, 15, 30)", name="check_periodo_valido"),
    )
    
    def __repr__(self):
        return f"<ReservaModel(id={self.id}, cliente_id={self.cliente_id}, status='{self.status}')>"
