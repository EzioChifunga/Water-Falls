"""
Entidades de domínio para Reservas e Pagamentos
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Reserva:
    """Entidade de domínio para Reserva"""
    id: Optional[str] = None
    cliente_id: str = ""
    veiculo_id: str = ""
    loja_retirada_id: str = ""
    loja_devolucao_id: str = ""
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    periodo: int = 0  # 7, 15 ou 30 dias
    valor_total: float = 0.0
    motorista_incluido: bool = False
    canal_origem: str = "WEB"  # WEB, LOJA, TELEFONE
    status: str = "PENDENTE_PAGAMENTO"  # PENDENTE_PAGAMENTO, CONFIRMADA, EM_CURSO, FINALIZADA, CANCELADA
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações básicas"""
        if not self.cliente_id:
            raise ValueError("Cliente é obrigatório")
        if not self.veiculo_id:
            raise ValueError("Veículo é obrigatório")
        if self.periodo not in [7, 15, 30]:
            raise ValueError("Período deve ser 7, 15 ou 30 dias")
        if self.valor_total < 0:
            raise ValueError("Valor total não pode ser negativo")
        valid_canais = ["WEB", "LOJA", "TELEFONE"]
        if self.canal_origem not in valid_canais:
            raise ValueError(f"Canal inválido. Deve ser um de: {valid_canais}")


@dataclass
class Pagamento:
    """Entidade de domínio para Pagamento"""
    id: Optional[str] = None
    reserva_id: str = ""
    metodo: str = "CARTAO"
    status: str = "PENDENTE"  # PAGO, PENDENTE, RECUSADO
    valor: float = 0.0
    transacao_gateway_id: Optional[str] = None
    criado_em: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações básicas"""
        if not self.reserva_id:
            raise ValueError("Reserva é obrigatória")
        if self.valor <= 0:
            raise ValueError("Valor deve ser maior que 0")
        valid_status = ["PAGO", "PENDENTE", "RECUSADO"]
        if self.status not in valid_status:
            raise ValueError(f"Status inválido. Deve ser um de: {valid_status}")
