"""
Repositório para operações com Reservas
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.reservas import Reserva
from app.infrastructure.models.reserva_model import ReservaModel


class ReservaRepository:
    """Repositório para gerenciar reservas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, reserva: Reserva) -> Reserva:
        """Cria uma nova reserva"""
        db_reserva = ReservaModel(
            cliente_id=reserva.cliente_id,
            veiculo_id=reserva.veiculo_id,
            loja_retirada_id=reserva.loja_retirada_id,
            loja_devolucao_id=reserva.loja_devolucao_id,
            data_inicio=reserva.data_inicio,
            data_fim=reserva.data_fim,
            periodo=reserva.periodo,
            valor_total=reserva.valor_total,
            motorista_incluido=reserva.motorista_incluido,
            canal_origem=reserva.canal_origem,
            status=reserva.status,
        )
        self.db.add(db_reserva)
        self.db.commit()
        self.db.refresh(db_reserva)
        return self._to_domain(db_reserva)
    
    def get_by_id(self, reserva_id: str) -> Optional[Reserva]:
        """Obtém uma reserva pelo ID"""
        db_reserva = self.db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        return self._to_domain(db_reserva) if db_reserva else None
    
    def get_by_cliente(self, cliente_id: str, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtém reservas de um cliente"""
        db_reservas = self.db.query(ReservaModel).filter(ReservaModel.cliente_id == cliente_id).offset(skip).limit(limit).all()
        return [self._to_domain(r) for r in db_reservas]
    
    def get_by_veiculo(self, veiculo_id: str, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtém reservas de um veículo"""
        db_reservas = self.db.query(ReservaModel).filter(ReservaModel.veiculo_id == veiculo_id).offset(skip).limit(limit).all()
        return [self._to_domain(r) for r in db_reservas]
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtém reservas por status"""
        db_reservas = self.db.query(ReservaModel).filter(ReservaModel.status == status).offset(skip).limit(limit).all()
        return [self._to_domain(r) for r in db_reservas]
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtém todas as reservas"""
        db_reservas = self.db.query(ReservaModel).offset(skip).limit(limit).all()
        return [self._to_domain(r) for r in db_reservas]
    
    def update(self, reserva_id: str, reserva: Reserva) -> Optional[Reserva]:
        """Atualiza uma reserva"""
        db_reserva = self.db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        if not db_reserva:
            return None
        
        db_reserva.cliente_id = reserva.cliente_id
        db_reserva.veiculo_id = reserva.veiculo_id
        db_reserva.loja_retirada_id = reserva.loja_retirada_id
        db_reserva.loja_devolucao_id = reserva.loja_devolucao_id
        db_reserva.data_inicio = reserva.data_inicio
        db_reserva.data_fim = reserva.data_fim
        db_reserva.periodo = reserva.periodo
        db_reserva.valor_total = reserva.valor_total
        db_reserva.motorista_incluido = reserva.motorista_incluido
        db_reserva.canal_origem = reserva.canal_origem
        db_reserva.status = reserva.status
        
        self.db.commit()
        self.db.refresh(db_reserva)
        return self._to_domain(db_reserva)
    
    def delete(self, reserva_id: str) -> bool:
        """Deleta uma reserva"""
        db_reserva = self.db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        if not db_reserva:
            return False
        
        self.db.delete(db_reserva)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_reserva: ReservaModel) -> Reserva:
        """Converte modelo ORM para entidade de domínio"""
        return Reserva(
            id=str(db_reserva.id),
            cliente_id=str(db_reserva.cliente_id),
            veiculo_id=str(db_reserva.veiculo_id),
            loja_retirada_id=str(db_reserva.loja_retirada_id),
            loja_devolucao_id=str(db_reserva.loja_devolucao_id),
            data_inicio=db_reserva.data_inicio,
            data_fim=db_reserva.data_fim,
            periodo=db_reserva.periodo,
            valor_total=float(db_reserva.valor_total),
            motorista_incluido=db_reserva.motorista_incluido,
            canal_origem=db_reserva.canal_origem,
            status=db_reserva.status,
            criado_em=db_reserva.criado_em,
            atualizado_em=db_reserva.atualizado_em,
        )
