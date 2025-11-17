"""
Entidades de domínio para Veículos e Categorias
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CategoriaVeiculo:
    """Entidade de categoria de veículo"""
    id: Optional[str] = None
    nome: str = ""
    
    def __post_init__(self):
        if not self.nome:
            raise ValueError("Nome é obrigatório")


@dataclass
class Veiculo:
    """Entidade de domínio para Veículo"""
    id: Optional[str] = None
    placa: str = ""
    marca: str = ""
    modelo: str = ""
    ano: int = 0
    image_url: Optional[str] = None
    categoria_id: str = ""
    diaria: float = 0.0
    status: str = "DISPONIVEL"  # DISPONIVEL, ALUGADO, RESERVADO, MANUTENCAO, FORA_AREA
    loja_id: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cor: Optional[str] = None
    combustivel: Optional[str] = None
    portas: Optional[int] = None
    cambio: Optional[str] = None
    quilometragem: Optional[float] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações básicas"""
        if not self.placa or len(self.placa) != 7:
            raise ValueError("Placa é obrigatória e deve ter 7 caracteres")
        if not self.marca:
            raise ValueError("Marca é obrigatória")
        if not self.modelo:
            raise ValueError("Modelo é obrigatório")
        if self.ano <= 0:
            raise ValueError("Ano deve ser maior que 0")
        if self.diaria <= 0:
            raise ValueError("Diária deve ser maior que 0")
        valid_status = ["DISPONIVEL", "ALUGADO", "RESERVADO", "MANUTENCAO", "FORA_AREA"]
        if self.status not in valid_status:
            raise ValueError(f"Status inválido. Deve ser um de: {valid_status}")


@dataclass
class HistoricoStatusVeiculo:
    """Entidade de domínio para Histórico de Status de Veículo"""
    id: Optional[str] = None
    veiculo_id: str = ""
    status_anterior: Optional[str] = None
    status_atual: str = "DISPONIVEL"
    data_mudanca: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações básicas"""
        if not self.veiculo_id:
            raise ValueError("Veículo é obrigatório")
        valid_status = ["DISPONIVEL", "ALUGADO", "RESERVADO", "MANUTENCAO", "FORA_AREA"]
        if self.status_atual not in valid_status:
            raise ValueError(f"Status atual inválido. Deve ser um de: {valid_status}")
        if self.status_anterior and self.status_anterior not in valid_status:
            raise ValueError(f"Status anterior inválido. Deve ser um de: {valid_status}")
