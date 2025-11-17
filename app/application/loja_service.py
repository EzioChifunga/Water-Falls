"""
Serviço de negócio para Lojas
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.lojas import Loja
from app.infrastructure.repositories.loja_repository import LojaRepository


class LojaService:
    """Serviço para gerenciar lojas"""
    
    def __init__(self, db: Session):
        self.repository = LojaRepository(db)
    
    def create_loja(self, nome: str, telefone: str, endereco_id: str) -> Loja:
        """Cria uma nova loja"""
        loja = Loja(
            nome=nome,
            telefone=telefone,
            endereco_id=endereco_id,
        )
        return self.repository.create(loja)
    
    def get_loja(self, loja_id: str) -> Optional[Loja]:
        """Obtém uma loja pelo ID"""
        return self.repository.get_by_id(loja_id)
    
    def get_all_lojas(self, skip: int = 0, limit: int = 100) -> List[Loja]:
        """Obtém todas as lojas"""
        return self.repository.get_all(skip, limit)
    
    def update_loja(self, loja_id: str, nome: str, telefone: str, endereco_id: str) -> Optional[Loja]:
        """Atualiza uma loja"""
        loja = Loja(
            nome=nome,
            telefone=telefone,
            endereco_id=endereco_id,
        )
        return self.repository.update(loja_id, loja)
    
    def delete_loja(self, loja_id: str) -> bool:
        """Deleta uma loja"""
        return self.repository.delete(loja_id)
