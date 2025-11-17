"""
Repositório para operações com Endereços
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.clientes import Endereco
from app.infrastructure.models.endereco_model import EnderecoModel


class EnderecoRepository:
    """Repositório para gerenciar endereços"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, endereco: Endereco) -> Endereco:
        """Cria um novo endereço"""
        db_endereco = EnderecoModel(
            rua=endereco.rua,
            cidade=endereco.cidade,
            estado=endereco.estado,
            latitude=endereco.latitude,
            longitude=endereco.longitude,
        )
        self.db.add(db_endereco)
        self.db.commit()
        self.db.refresh(db_endereco)
        return self._to_domain(db_endereco)
    
    def get_by_id(self, endereco_id: str) -> Optional[Endereco]:
        """Obtém um endereço pelo ID"""
        db_endereco = self.db.query(EnderecoModel).filter(EnderecoModel.id == endereco_id).first()
        return self._to_domain(db_endereco) if db_endereco else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Endereco]:
        """Obtém todos os endereços"""
        db_enderecos = self.db.query(EnderecoModel).offset(skip).limit(limit).all()
        return [self._to_domain(e) for e in db_enderecos]
    
    def update(self, endereco_id: str, endereco: Endereco) -> Optional[Endereco]:
        """Atualiza um endereço"""
        db_endereco = self.db.query(EnderecoModel).filter(EnderecoModel.id == endereco_id).first()
        if not db_endereco:
            return None
        
        db_endereco.rua = endereco.rua
        db_endereco.cidade = endereco.cidade
        db_endereco.estado = endereco.estado
        db_endereco.latitude = endereco.latitude
        db_endereco.longitude = endereco.longitude
        
        self.db.commit()
        self.db.refresh(db_endereco)
        return self._to_domain(db_endereco)
    
    def delete(self, endereco_id: str) -> bool:
        """Deleta um endereço"""
        db_endereco = self.db.query(EnderecoModel).filter(EnderecoModel.id == endereco_id).first()
        if not db_endereco:
            return False
        
        self.db.delete(db_endereco)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_endereco: EnderecoModel) -> Endereco:
        """Converte modelo ORM para entidade de domínio"""
        return Endereco(
            id=str(db_endereco.id),
            rua=db_endereco.rua,
            cidade=db_endereco.cidade,
            estado=db_endereco.estado,
            latitude=float(db_endereco.latitude) if db_endereco.latitude else None,
            longitude=float(db_endereco.longitude) if db_endereco.longitude else None,
        )
