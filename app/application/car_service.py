"""
Serviço de aplicação para gerenciar casos de uso de Carros
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.cars import Car
from app.infrastructure.repositories.car_repository import CarRepository


class CarService:
    """Serviço de aplicação para operações com carros"""
    
    def __init__(self, db: Session):
        self.repository = CarRepository(db)
    
    def create_car(self, brand: str, model: str, year: int, color: str, plate: str) -> Car:
        """
        Caso de uso: Criar um novo carro
        """
        # Validações de negócio
        existing_car = self.repository.get_by_plate(plate)
        if existing_car:
            raise ValueError(f"Já existe um carro com a placa {plate}")
        
        # Criar a entidade de domínio
        car = Car(
            brand=brand,
            model=model,
            year=year,
            color=color,
            plate=plate,
        )
        
        # Persistir no banco de dados
        return self.repository.create(car)
    
    def get_car(self, car_id: int) -> Optional[Car]:
        """
        Caso de uso: Obter um carro pelo ID
        """
        return self.repository.get_by_id(car_id)
    
    def get_all_cars(self, skip: int = 0, limit: int = 100) -> List[Car]:
        """
        Caso de uso: Obter todos os carros com paginação
        """
        return self.repository.get_all(skip=skip, limit=limit)
    
    def update_car(self, car_id: int, brand: str, model: str, year: int, color: str, plate: str) -> Optional[Car]:
        """
        Caso de uso: Atualizar um carro existente
        """
        # Validação: verificar se placa já existe em outro carro
        existing_car = self.repository.get_by_plate(plate)
        if existing_car and existing_car.id != car_id:
            raise ValueError(f"Já existe outro carro com a placa {plate}")
        
        car = Car(
            brand=brand,
            model=model,
            year=year,
            color=color,
            plate=plate,
        )
        
        return self.repository.update(car_id, car)
    
    def delete_car(self, car_id: int) -> bool:
        """
        Caso de uso: Deletar um carro
        """
        return self.repository.delete(car_id)
