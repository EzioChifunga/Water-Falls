"""
Repositório para operações com Categorias de Veículos
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.veiculos import CategoriaVeiculo
from app.infrastructure.models.categoria_veiculo_model import CategoriaVeiculoModel


class CategoriaVeiculoRepository:
    """Repositório para gerenciar categorias de veículos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, categoria: CategoriaVeiculo) -> CategoriaVeiculo:
        """Cria uma nova categoria"""
        db_categoria = CategoriaVeiculoModel(nome=categoria.nome)
        self.db.add(db_categoria)
        self.db.commit()
        self.db.refresh(db_categoria)
        return self._to_domain(db_categoria)
    
    def get_by_id(self, categoria_id: str) -> Optional[CategoriaVeiculo]:
        """Obtém uma categoria pelo ID"""
        try:
            _id = uuid.UUID(str(categoria_id))
        except Exception:
            return None
        db_categoria = self.db.query(CategoriaVeiculoModel).filter(CategoriaVeiculoModel.id == _id).first()
        return self._to_domain(db_categoria) if db_categoria else None
    
    def get_by_nome(self, nome: str) -> Optional[CategoriaVeiculo]:
        """Obtém uma categoria pelo nome"""
        db_categoria = self.db.query(CategoriaVeiculoModel).filter(CategoriaVeiculoModel.nome == nome).first()
        return self._to_domain(db_categoria) if db_categoria else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[CategoriaVeiculo]:
        """Obtém todas as categorias"""
        db_categorias = self.db.query(CategoriaVeiculoModel).offset(skip).limit(limit).all()
        return [self._to_domain(c) for c in db_categorias]
    
    def update(self, categoria_id: str, categoria: CategoriaVeiculo) -> Optional[CategoriaVeiculo]:
        """Atualiza uma categoria"""
        try:
            _id = uuid.UUID(str(categoria_id))
        except Exception:
            return None
        db_categoria = self.db.query(CategoriaVeiculoModel).filter(CategoriaVeiculoModel.id == _id).first()
        if not db_categoria:
            return None
        
        db_categoria.nome = categoria.nome
        self.db.commit()
        self.db.refresh(db_categoria)
        return self._to_domain(db_categoria)
    
    def delete(self, categoria_id: str) -> bool:
        """Deleta uma categoria"""
        try:
            _id = uuid.UUID(str(categoria_id))
        except Exception:
            return False
        db_categoria = self.db.query(CategoriaVeiculoModel).filter(CategoriaVeiculoModel.id == _id).first()
        if not db_categoria:
            return False
        
        self.db.delete(db_categoria)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_categoria: CategoriaVeiculoModel) -> CategoriaVeiculo:
        """Converte modelo ORM para entidade de domínio"""
        return CategoriaVeiculo(
            id=str(db_categoria.id),
            nome=db_categoria.nome,
        )
