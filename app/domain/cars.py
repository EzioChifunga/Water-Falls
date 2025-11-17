"""
Entidades e interfaces de domínio para Carros
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Car:
    """Entidade de domínio para Carro"""
    
    id: Optional[int] = None
    brand: str = ""
    model: str = ""
    year: int = 0
    color: str = ""
    plate: str = ""
    
    def __post_init__(self):
        """Validações básicas após inicialização"""
        if not self.brand:
            raise ValueError("Brand é obrigatório")
        if not self.model:
            raise ValueError("Model é obrigatório")
        if self.year <= 0:
            raise ValueError("Year deve ser maior que 0")
        if not self.plate:
            raise ValueError("Plate é obrigatório")
