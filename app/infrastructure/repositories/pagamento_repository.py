"""
Repositório para operações com Pagamentos
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.reservas import Pagamento
from app.infrastructure.models.pagamento_model import PagamentoModel


class PagamentoRepository:
    """Repositório para gerenciar pagamentos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, pagamento: Pagamento) -> Pagamento:
        """Cria um novo pagamento"""
        try:
            _reserva_id = uuid.UUID(str(pagamento.reserva_id))
        except Exception:
            raise ValueError("Reserva ID inválido")
        
        db_pagamento = PagamentoModel(
            reserva_id=_reserva_id,
            metodo=pagamento.metodo,
            status=pagamento.status,
            valor=pagamento.valor,
            transacao_gateway_id=pagamento.transacao_gateway_id,
        )
        self.db.add(db_pagamento)
        self.db.commit()
        self.db.refresh(db_pagamento)
        return self._to_domain(db_pagamento)
    
    def get_by_id(self, pagamento_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pelo ID"""
        try:
            _id = uuid.UUID(str(pagamento_id))
        except Exception:
            return None
        db_pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.id == _id).first()
        return self._to_domain(db_pagamento) if db_pagamento else None
    
    def get_by_reserva(self, reserva_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pela reserva"""
        try:
            _id = uuid.UUID(str(reserva_id))
        except Exception:
            return None
        db_pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.reserva_id == _id).first()
        return self._to_domain(db_pagamento) if db_pagamento else None
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Pagamento]:
        """Obtém pagamentos por status"""
        db_pagamentos = self.db.query(PagamentoModel).filter(PagamentoModel.status == status).offset(skip).limit(limit).all()
        return [self._to_domain(p) for p in db_pagamentos]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pagamento]:
        """Obtém todos os pagamentos"""
        db_pagamentos = self.db.query(PagamentoModel).offset(skip).limit(limit).all()
        return [self._to_domain(p) for p in db_pagamentos]
    
    def update(self, pagamento_id: str, pagamento: Pagamento) -> Optional[Pagamento]:
        """Atualiza um pagamento"""
        try:
            _id = uuid.UUID(str(pagamento_id))
        except Exception:
            return None
        db_pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.id == _id).first()
        if not db_pagamento:
            return None
        
        db_pagamento.metodo = pagamento.metodo
        db_pagamento.status = pagamento.status
        db_pagamento.valor = pagamento.valor
        db_pagamento.transacao_gateway_id = pagamento.transacao_gateway_id
        
        self.db.commit()
        self.db.refresh(db_pagamento)
        return self._to_domain(db_pagamento)
    
    def delete(self, pagamento_id: str) -> bool:
        """Deleta um pagamento"""
        try:
            _id = uuid.UUID(str(pagamento_id))
        except Exception:
            return False
        db_pagamento = self.db.query(PagamentoModel).filter(PagamentoModel.id == _id).first()
        if not db_pagamento:
            return False
        
        self.db.delete(db_pagamento)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_pagamento: PagamentoModel) -> Pagamento:
        """Converte modelo ORM para entidade de domínio"""
        return Pagamento(
            id=str(db_pagamento.id),
            reserva_id=str(db_pagamento.reserva_id),
            metodo=db_pagamento.metodo,
            status=db_pagamento.status,
            valor=float(db_pagamento.valor),
            transacao_gateway_id=db_pagamento.transacao_gateway_id,
            criado_em=db_pagamento.criado_em,
        )

