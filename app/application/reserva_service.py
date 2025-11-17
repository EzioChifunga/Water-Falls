"""
Serviço de aplicação para gerenciar Reservas
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.domain.reservas import Reserva
from app.infrastructure.repositories.reserva_repository import ReservaRepository
from app.infrastructure.repositories.cliente_repository import ClienteRepository
from app.infrastructure.repositories.veiculo_repository import VeiculoRepository


class ReservaService:
    """Serviço de aplicação para operações com reservas"""
    
    def __init__(self, db: Session):
        self.reserva_repo = ReservaRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.veiculo_repo = VeiculoRepository(db)
    
    def create_reserva(self, cliente_id: str, veiculo_id: str, loja_retirada_id: str,
                       loja_devolucao_id: str, data_inicio: date, data_fim: date,
                       periodo: int, valor_total: float, motorista_incluido: bool = False,
                       canal_origem: str = "WEB") -> Reserva:
        """Criar uma nova reserva"""
        
        # Validações
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} não encontrado")
        
        veiculo = self.veiculo_repo.get_by_id(veiculo_id)
        if not veiculo:
            raise ValueError(f"Veículo {veiculo_id} não encontrado")
        
        if veiculo.status != "DISPONIVEL":
            raise ValueError(f"Veículo não está disponível. Status: {veiculo.status}")
        
        if periodo not in [7, 15, 30]:
            raise ValueError("Período deve ser 7, 15 ou 30 dias")
        
        if valor_total <= 0:
            raise ValueError("Valor total deve ser maior que 0")
        
        reserva = Reserva(
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            loja_retirada_id=loja_retirada_id,
            loja_devolucao_id=loja_devolucao_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            periodo=periodo,
            valor_total=valor_total,
            motorista_incluido=motorista_incluido,
            canal_origem=canal_origem,
            status="PENDENTE_PAGAMENTO",
        )
        
        return self.reserva_repo.create(reserva)
    
    def get_reserva(self, reserva_id: str) -> Optional[Reserva]:
        """Obter uma reserva pelo ID"""
        return self.reserva_repo.get_by_id(reserva_id)
    
    def get_reservas_cliente(self, cliente_id: str, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obter reservas de um cliente"""
        return self.reserva_repo.get_by_cliente(cliente_id, skip=skip, limit=limit)
    
    def get_reservas_veiculo(self, veiculo_id: str, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obter reservas de um veículo"""
        return self.reserva_repo.get_by_veiculo(veiculo_id, skip=skip, limit=limit)
    
    def get_all_reservas(self, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obter todas as reservas"""
        return self.reserva_repo.get_all(skip=skip, limit=limit)
    
    def confirmar_reserva(self, reserva_id: str) -> Optional[Reserva]:
        """Confirmar uma reserva (após pagamento)"""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            return None
        
        reserva.status = "CONFIRMADA"
        
        # Atualizar status do veículo para ALUGADO
        veiculo = self.veiculo_repo.get_by_id(reserva.veiculo_id)
        if veiculo:
            veiculo.status = "ALUGADO"
            self.veiculo_repo.update(reserva.veiculo_id, veiculo)
        
        return self.reserva_repo.update(reserva_id, reserva)
    
    def cancelar_reserva(self, reserva_id: str) -> Optional[Reserva]:
        """Cancelar uma reserva"""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            return None
        
        reserva.status = "CANCELADA"
        
        # Atualizar status do veículo para DISPONIVEL se estava alugado
        veiculo = self.veiculo_repo.get_by_id(reserva.veiculo_id)
        if veiculo and veiculo.status == "ALUGADO":
            veiculo.status = "DISPONIVEL"
            self.veiculo_repo.update(reserva.veiculo_id, veiculo)
        
        return self.reserva_repo.update(reserva_id, reserva)
    
    def delete_reserva(self, reserva_id: str) -> bool:
        """Deletar uma reserva"""
        return self.reserva_repo.delete(reserva_id)
