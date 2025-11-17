"""
Repositório para operações com Lojas
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.lojas import Loja
from app.infrastructure.models.loja_model import LojaModel


class LojaRepository:
    """Repositório para gerenciar lojas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, loja: Loja) -> Loja:
        """Cria uma nova loja"""
        try:
            _endereco_id = uuid.UUID(str(loja.endereco_id))
        except Exception:
            raise ValueError("Endereço ID inválido")
        
        db_loja = LojaModel(
            nome=loja.nome,
            telefone=loja.telefone,
            endereco_id=_endereco_id,
        )
        self.db.add(db_loja)
        self.db.commit()
        self.db.refresh(db_loja)
        return self._to_domain(db_loja)
    
    def get_by_id(self, loja_id: str) -> Optional[Loja]:
        """Obtém uma loja pelo ID"""
        try:
            _id = uuid.UUID(str(loja_id))
        except Exception:
            return None
        db_loja = self.db.query(LojaModel).filter(LojaModel.id == _id).first()
        return self._to_domain(db_loja) if db_loja else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Loja]:
        """Obtém todas as lojas"""
        db_lojas = self.db.query(LojaModel).offset(skip).limit(limit).all()
        return [self._to_domain(l) for l in db_lojas]
    
    def update(self, loja_id: str, loja: Loja) -> Optional[Loja]:
        """Atualiza uma loja"""
        try:
            _id = uuid.UUID(str(loja_id))
        except Exception:
            return None
        db_loja = self.db.query(LojaModel).filter(LojaModel.id == _id).first()
        if not db_loja:
            return None
        
        db_loja.nome = loja.nome
        db_loja.telefone = loja.telefone
        try:
            db_loja.endereco_id = uuid.UUID(str(loja.endereco_id))
        except Exception:
            return None
        
        self.db.commit()
        self.db.refresh(db_loja)
        return self._to_domain(db_loja)
    
    def delete(self, loja_id: str) -> bool:
        """Deleta uma loja"""
        try:
            _id = uuid.UUID(str(loja_id))
        except Exception:
            return False
        db_loja = self.db.query(LojaModel).filter(LojaModel.id == _id).first()
        if not db_loja:
            return False
        
        self.db.delete(db_loja)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_loja: LojaModel) -> Loja:
        """Converte modelo ORM para entidade de domínio"""
        return Loja(
            id=str(db_loja.id),
            nome=db_loja.nome,
            telefone=db_loja.telefone,
            endereco_id=str(db_loja.endereco_id),
        )
