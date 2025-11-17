"""
Repositório para operações com Carros no banco de dados
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.cars import Car
from app.infrastructure.models.car_model import CarModel


class CarRepository:
    """Repositório para gerenciar carros no banco de dados"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, car: Car) -> Car:
        """
        Cria um novo carro no banco de dados
        """
        db_car = CarModel(
            brand=car.brand,
            model=car.model,
            year=car.year,
            color=car.color,
            plate=car.plate,
        )
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return self._to_domain(db_car)
    
    def get_by_id(self, car_id: int) -> Optional[Car]:
        """
        Obtém um carro pelo ID
        """
        db_car = self.db.query(CarModel).filter(CarModel.id == car_id).first()
        return self._to_domain(db_car) if db_car else None
    
    def get_by_plate(self, plate: str) -> Optional[Car]:
        """
        Obtém um carro pela placa
        """
        db_car = self.db.query(CarModel).filter(CarModel.plate == plate).first()
        return self._to_domain(db_car) if db_car else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Car]:
        """
        Obtém todos os carros com paginação
        """
        db_cars = self.db.query(CarModel).offset(skip).limit(limit).all()
        return [self._to_domain(car) for car in db_cars]
    
    def update(self, car_id: int, car: Car) -> Optional[Car]:
        """
        Atualiza um carro existente
        """
        db_car = self.db.query(CarModel).filter(CarModel.id == car_id).first()
        if not db_car:
            return None
        
        db_car.brand = car.brand
        db_car.model = car.model
        db_car.year = car.year
        db_car.color = car.color
        db_car.plate = car.plate
        
        self.db.commit()
        self.db.refresh(db_car)
        return self._to_domain(db_car)
    
    def delete(self, car_id: int) -> bool:
        """
        Deleta um carro
        """
        db_car = self.db.query(CarModel).filter(CarModel.id == car_id).first()
        if not db_car:
            return False
        
        self.db.delete(db_car)
        self.db.commit()
        return True
    
    @staticmethod
    def _to_domain(db_car: CarModel) -> Car:
        """Converte modelo ORM para entidade de domínio"""
        return Car(
            id=db_car.id,
            brand=db_car.brand,
            model=db_car.model,
            year=db_car.year,
            color=db_car.color,
            plate=db_car.plate,
        )
