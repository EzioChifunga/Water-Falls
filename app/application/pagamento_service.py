"""
Serviço de negócio para Pagamentos
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.reservas import Pagamento
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository


class PagamentoService:
    """Serviço para gerenciar pagamentos"""
    
    def __init__(self, db: Session):
        self.repository = PagamentoRepository(db)
    
    def create_pagamento(self, reserva_id: str, metodo: str, status: str, valor: float, transacao_gateway_id: Optional[str] = None) -> Pagamento:
        """Cria um novo pagamento"""
        pagamento = Pagamento(
            reserva_id=reserva_id,
            metodo=metodo,
            status=status,
            valor=valor,
            transacao_gateway_id=transacao_gateway_id,
        )
        return self.repository.create(pagamento)
    
    def get_pagamento(self, pagamento_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pelo ID"""
        return self.repository.get_by_id(pagamento_id)
    
    def get_pagamento_by_reserva(self, reserva_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pela reserva"""
        return self.repository.get_by_reserva(reserva_id)
    
    def get_pagamentos_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Pagamento]:
        """Obtém pagamentos por status"""
        return self.repository.get_by_status(status, skip, limit)
    
    def get_all_pagamentos(self, skip: int = 0, limit: int = 100) -> List[Pagamento]:
        """Obtém todos os pagamentos"""
        return self.repository.get_all(skip, limit)
    
    def update_pagamento(self, pagamento_id: str, metodo: str, status: str, valor: float, transacao_gateway_id: Optional[str] = None) -> Optional[Pagamento]:
        """Atualiza um pagamento"""
        pagamento = Pagamento(
            reserva_id="",  # não será alterado
            metodo=metodo,
            status=status,
            valor=valor,
            transacao_gateway_id=transacao_gateway_id,
        )
        # Precisa recuperar o pagamento original para manter reserva_id
        original = self.repository.get_by_id(pagamento_id)
        if not original:
            return None
        pagamento.reserva_id = original.reserva_id
        return self.repository.update(pagamento_id, pagamento)
    
    def delete_pagamento(self, pagamento_id: str) -> bool:
        """Deleta um pagamento"""
        return self.repository.delete(pagamento_id)
