"""
Serviço de negócio para Endereços
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.clientes import Endereco
from app.infrastructure.repositories.endereco_repository import EnderecoRepository


class EnderecoService:
    """Serviço para gerenciar endereços"""
    
    def __init__(self, db: Session):
        self.repository = EnderecoRepository(db)
    
    def create_endereco(self, rua: str, cidade: str, estado: str, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Endereco:
        """Cria um novo endereço"""
        endereco = Endereco(
            rua=rua,
            cidade=cidade,
            estado=estado,
            latitude=latitude,
            longitude=longitude,
        )
        return self.repository.create(endereco)
    
    def get_endereco(self, endereco_id: str) -> Optional[Endereco]:
        """Obtém um endereço pelo ID"""
        return self.repository.get_by_id(endereco_id)
    
    def get_all_enderecos(self, skip: int = 0, limit: int = 100) -> List[Endereco]:
        """Obtém todos os endereços"""
        return self.repository.get_all(skip, limit)
    
    def update_endereco(self, endereco_id: str, rua: str, cidade: str, estado: str, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Optional[Endereco]:
        """Atualiza um endereço"""
        endereco = Endereco(
            rua=rua,
            cidade=cidade,
            estado=estado,
            latitude=latitude,
            longitude=longitude,
        )
        return self.repository.update(endereco_id, endereco)
    
    def delete_endereco(self, endereco_id: str) -> bool:
        """Deleta um endereço"""
        return self.repository.delete(endereco_id)
