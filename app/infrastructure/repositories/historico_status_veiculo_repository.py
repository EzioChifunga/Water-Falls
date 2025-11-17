"""
Repositório para operações com Histórico de Status de Veículo
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.veiculos import HistoricoStatusVeiculo
from app.infrastructure.models.historico_status_veiculo_model import HistoricoStatusVeiculoModel


class HistoricoStatusVeiculoRepository:
    """Repositório para gerenciar histórico de status de veículos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, historico: HistoricoStatusVeiculo) -> HistoricoStatusVeiculo:
        """Cria um novo registro de histórico"""
        db_historico = HistoricoStatusVeiculoModel(
            veiculo_id=historico.veiculo_id,
            status_anterior=historico.status_anterior,
            status_atual=historico.status_atual,
        )
        self.db.add(db_historico)
        self.db.commit()
        self.db.refresh(db_historico)
        return self._to_domain(db_historico)
    
    def get_by_id(self, historico_id: str) -> Optional[HistoricoStatusVeiculo]:
        """Obtém um histórico pelo ID"""
        try:
            _id = uuid.UUID(str(historico_id))
        except Exception:
            return None
        db_historico = self.db.query(HistoricoStatusVeiculoModel).filter(HistoricoStatusVeiculoModel.id == _id).first()
        return self._to_domain(db_historico) if db_historico else None
    
    def get_by_veiculo(self, veiculo_id: str, skip: int = 0, limit: int = 100) -> List[HistoricoStatusVeiculo]:
        """Obtém todos os históricos de um veículo"""
        try:
            _id = uuid.UUID(str(veiculo_id))
        except Exception:
            return []
        db_historicos = self.db.query(HistoricoStatusVeiculoModel).filter(
            HistoricoStatusVeiculoModel.veiculo_id == _id
        ).offset(skip).limit(limit).all()
        return [self._to_domain(h) for h in db_historicos]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[HistoricoStatusVeiculo]:
        """Obtém todos os históricos"""
        db_historicos = self.db.query(HistoricoStatusVeiculoModel).offset(skip).limit(limit).all()
        return [self._to_domain(h) for h in db_historicos]
    
    @staticmethod
    def _to_domain(db_historico: HistoricoStatusVeiculoModel) -> HistoricoStatusVeiculo:
        """Converte modelo ORM para entidade de domínio"""
        return HistoricoStatusVeiculo(
            id=str(db_historico.id),
            veiculo_id=str(db_historico.veiculo_id),
            status_anterior=db_historico.status_anterior,
            status_atual=db_historico.status_atual,
            data_mudanca=db_historico.data_mudanca,
        )
