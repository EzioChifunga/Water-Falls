"""
Serviço de negócio para Histórico de Status de Veículo
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.veiculos import HistoricoStatusVeiculo
from app.infrastructure.repositories.historico_status_veiculo_repository import HistoricoStatusVeiculoRepository


class HistoricoStatusVeiculoService:
    """Serviço para gerenciar histórico de status de veículos"""
    
    def __init__(self, db: Session):
        self.repository = HistoricoStatusVeiculoRepository(db)
    
    def create_historico(self, veiculo_id: str, status_anterior: Optional[str], status_atual: str) -> HistoricoStatusVeiculo:
        """Cria um novo registro de histórico"""
        historico = HistoricoStatusVeiculo(
            veiculo_id=veiculo_id,
            status_anterior=status_anterior,
            status_atual=status_atual,
        )
        return self.repository.create(historico)
    
    def get_historico(self, historico_id: str) -> Optional[HistoricoStatusVeiculo]:
        """Obtém um histórico pelo ID"""
        return self.repository.get_by_id(historico_id)
    
    def get_historicos_veiculo(self, veiculo_id: str, skip: int = 0, limit: int = 100) -> List[HistoricoStatusVeiculo]:
        """Obtém todos os históricos de um veículo"""
        return self.repository.get_by_veiculo(veiculo_id, skip, limit)
    
    def get_all_historicos(self, skip: int = 0, limit: int = 100) -> List[HistoricoStatusVeiculo]:
        """Obtém todos os históricos"""
        return self.repository.get_all(skip, limit)
