"""
Serviço de negócio para Categorias de Veículos
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.veiculos import CategoriaVeiculo
from app.infrastructure.repositories.categoria_veiculo_repository import CategoriaVeiculoRepository


class CategoriaVeiculoService:
    """Serviço para gerenciar categorias de veículos"""
    
    def __init__(self, db: Session):
        self.repository = CategoriaVeiculoRepository(db)
    
    def create_categoria(self, nome: str) -> CategoriaVeiculo:
        """Cria uma nova categoria"""
        categoria = CategoriaVeiculo(nome=nome)
        return self.repository.create(categoria)
    
    def get_categoria(self, categoria_id: str) -> Optional[CategoriaVeiculo]:
        """Obtém uma categoria pelo ID"""
        return self.repository.get_by_id(categoria_id)
    
    def get_categoria_by_nome(self, nome: str) -> Optional[CategoriaVeiculo]:
        """Obtém uma categoria pelo nome"""
        return self.repository.get_by_nome(nome)
    
    def get_all_categorias(self, skip: int = 0, limit: int = 100) -> List[CategoriaVeiculo]:
        """Obtém todas as categorias"""
        return self.repository.get_all(skip, limit)
    
    def update_categoria(self, categoria_id: str, nome: str) -> Optional[CategoriaVeiculo]:
        """Atualiza uma categoria"""
        categoria = CategoriaVeiculo(nome=nome)
        return self.repository.update(categoria_id, categoria)
    
    def delete_categoria(self, categoria_id: str) -> bool:
        """Deleta uma categoria"""
        return self.repository.delete(categoria_id)
