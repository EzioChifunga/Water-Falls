"""
Entidades de domínio para Lojas
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Loja:
    """Entidade de domínio para Loja"""
    id: Optional[str] = None
    nome: str = ""
    telefone: str = ""
    endereco_id: str = ""
    
    def __post_init__(self):
        """Validações básicas"""
        if not self.nome:
            raise ValueError("Nome é obrigatório")
        if not self.endereco_id:
            raise ValueError("Endereço é obrigatório")
