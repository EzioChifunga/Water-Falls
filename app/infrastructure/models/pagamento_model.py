"""
Modelo ORM para Pagamentos
"""
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from app.infrastructure.config.database import Base


class PagamentoModel(Base):
    """Modelo de banco de dados para Pagamento"""
    
    __tablename__ = "pagamentos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reserva_id = Column(UUID(as_uuid=True), ForeignKey("reservas.id"), nullable=False, unique=True)
    metodo = Column(
        ENUM('CARTAO', name='metodo_pagamento'),
        nullable=False,
        default='CARTAO'
    )
    status = Column(
        ENUM('PAGO', 'PENDENTE', 'RECUSADO', name='status_pagamento'),
        nullable=False,
        default='PENDENTE'
    )
    valor = Column(Numeric(10, 2), nullable=False)
    transacao_gateway_id = Column(String(120), nullable=True, unique=True)
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<PagamentoModel(id={self.id}, status='{self.status}', valor={self.valor})>"
