"""
Entidades de domínio para Clientes
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Endereco:
    """Entidade de endereço"""
    id: Optional[str] = None
    rua: str = ""
    cidade: str = ""
    estado: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class Cliente:
    """Entidade de domínio para Cliente"""
    id: Optional[str] = None
    nome: str = ""
    cpf: str = ""
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco_id: Optional[str] = None
    cnh_numero: str = ""
    cnh_validade: Optional[str] = None  # DATE em string
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações básicas após inicialização"""
        if not self.nome:
            raise ValueError("Nome é obrigatório")
        if not self.cpf or len(self.cpf) != 11:
            raise ValueError("CPF é obrigatório e deve ter 11 dígitos")
        if not self.cnh_numero:
            raise ValueError("CNH número é obrigatório")
        if not self.cnh_validade:
            raise ValueError("CNH validade é obrigatória")
