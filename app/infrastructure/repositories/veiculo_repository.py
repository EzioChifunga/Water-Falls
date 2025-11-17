"""
Repositório para operações com Veículos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.veiculos import Veiculo
from app.infrastructure.models.veiculo_model import VeiculoModel


class VeiculoRepository:
    """Repositório para gerenciar veículos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, veiculo: Veiculo) -> Veiculo:
        """Cria um novo veículo"""
        db_veiculo = VeiculoModel(
            placa=veiculo.placa,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
            cor=veiculo.cor,
            combustivel=veiculo.combustivel,
            portas=veiculo.portas,
            cambio=veiculo.cambio,
            quilometragem=veiculo.quilometragem,
            categoria_id=(__import__('uuid').UUID(str(veiculo.categoria_id)) if veiculo.categoria_id else None),
            diaria=veiculo.diaria,
            status=veiculo.status,
            loja_id=(__import__('uuid').UUID(str(veiculo.loja_id)) if veiculo.loja_id else None),
            latitude=veiculo.latitude,
            longitude=veiculo.longitude,
        )
        self.db.add(db_veiculo)
        self.db.commit()
        self.db.refresh(db_veiculo)
        return self._to_domain(db_veiculo)
    
    def get_by_id(self, veiculo_id: str) -> Optional[Veiculo]:
        """Obtém um veículo pelo ID"""
        try:
            import uuid
            _id = uuid.UUID(str(veiculo_id))
        except Exception:
            return None
        db_veiculo = self.db.query(VeiculoModel).filter(VeiculoModel.id == _id).first()
        return self._to_domain(db_veiculo) if db_veiculo else None
    
    def get_by_placa(self, placa: str) -> Optional[Veiculo]:
        """Obtém um veículo pela placa"""
        db_veiculo = self.db.query(VeiculoModel).filter(VeiculoModel.placa == placa).first()
        return self._to_domain(db_veiculo) if db_veiculo else None
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obtém veículos por status"""
        db_veiculos = self.db.query(VeiculoModel).filter(VeiculoModel.status == status).offset(skip).limit(limit).all()
        return [self._to_domain(v) for v in db_veiculos]
    
    def get_by_loja(self, loja_id: str, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obtém veículos de uma loja"""
        try:
            import uuid
            _id = uuid.UUID(str(loja_id))
        except Exception:
            return []
        db_veiculos = self.db.query(VeiculoModel).filter(VeiculoModel.loja_id == _id).offset(skip).limit(limit).all()
        return [self._to_domain(v) for v in db_veiculos]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obtém todos os veículos"""
        db_veiculos = self.db.query(VeiculoModel).offset(skip).limit(limit).all()
        return [self._to_domain(v) for v in db_veiculos]
    
    def update(self, veiculo_id: str, veiculo: Veiculo) -> Optional[Veiculo]:
        """Atualiza um veículo"""
        try:
            import uuid
            _id = uuid.UUID(str(veiculo_id))
        except Exception:
            return None

        db_veiculo = self.db.query(VeiculoModel).filter(VeiculoModel.id == _id).first()
        if not db_veiculo:
            return None
        
        db_veiculo.placa = veiculo.placa
        db_veiculo.marca = veiculo.marca
        db_veiculo.modelo = veiculo.modelo
        db_veiculo.ano = veiculo.ano
        db_veiculo.cor = veiculo.cor
        db_veiculo.combustivel = veiculo.combustivel
        db_veiculo.portas = veiculo.portas
        db_veiculo.cambio = veiculo.cambio
        db_veiculo.quilometragem = veiculo.quilometragem
        db_veiculo.categoria_id = (__import__('uuid').UUID(str(veiculo.categoria_id)) if veiculo.categoria_id else None)
        db_veiculo.diaria = veiculo.diaria
        db_veiculo.status = veiculo.status
        db_veiculo.loja_id = (__import__('uuid').UUID(str(veiculo.loja_id)) if veiculo.loja_id else None)
        db_veiculo.latitude = veiculo.latitude
        db_veiculo.longitude = veiculo.longitude
        
        self.db.commit()
        self.db.refresh(db_veiculo)
        return self._to_domain(db_veiculo)
    
    def delete(self, veiculo_id: str) -> bool:
        """Deleta um veículo"""
        try:
            import uuid
            _id = uuid.UUID(str(veiculo_id))
        except Exception:
            return False
        db_veiculo = self.db.query(VeiculoModel).filter(VeiculoModel.id == _id).first()
        if not db_veiculo:
            return False
        
        self.db.delete(db_veiculo)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_veiculo: VeiculoModel) -> Veiculo:
        """Converte modelo ORM para entidade de domínio"""
        return Veiculo(
            id=str(db_veiculo.id),
            placa=db_veiculo.placa,
            marca=db_veiculo.marca,
            modelo=db_veiculo.modelo,
            ano=db_veiculo.ano,
            cor=db_veiculo.cor,
            combustivel=db_veiculo.combustivel,
            portas=db_veiculo.portas,
            cambio=db_veiculo.cambio,
            quilometragem=float(db_veiculo.quilometragem) if db_veiculo.quilometragem is not None else None,
            categoria_id=str(db_veiculo.categoria_id),
            diaria=float(db_veiculo.diaria),
            status=db_veiculo.status,
            loja_id=str(db_veiculo.loja_id),
            latitude=float(db_veiculo.latitude) if db_veiculo.latitude else None,
            longitude=float(db_veiculo.longitude) if db_veiculo.longitude else None,
            criado_em=db_veiculo.criado_em,
            atualizado_em=db_veiculo.atualizado_em,
        )
