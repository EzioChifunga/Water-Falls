"""
Controller/Rotas para gerenciar Carros
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.car_service import CarService


# Schema Pydantic para requisições/respostas
class CarCreate(BaseModel):
    """Schema para criar um carro"""
    brand: str
    model: str
    year: int
    color: str
    plate: str


class CarUpdate(BaseModel):
    """Schema para atualizar um carro"""
    brand: str
    model: str
    year: int
    color: str
    plate: str


class CarResponse(BaseModel):
    """Schema para resposta de carro"""
    id: int
    brand: str
    model: str
    year: int
    color: str
    plate: str
    
    class Config:
        from_attributes = True


# Router
router = APIRouter(
    prefix="/cars",
    tags=["cars"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CarResponse, status_code=201)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    """
    Endpoint para criar um novo carro
    
    - **brand**: Marca do carro
    - **model**: Modelo do carro
    - **year**: Ano de fabricação
    - **color**: Cor do carro
    - **plate**: Placa (única)
    """
    try:
        service = CarService(db)
        created_car = service.create_car(
            brand=car.brand,
            model=car.model,
            year=car.year,
            color=car.color,
            plate=car.plate,
        )
        return created_car
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obter um carro pelo ID
    """
    service = CarService(db)
    car = service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return car


@router.get("/", response_model=List[CarResponse])
def get_all_cars(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obter todos os carros com paginação
    
    - **skip**: Número de registros a pular (padrão: 0)
    - **limit**: Número máximo de registros (padrão: 100, máx: 1000)
    """
    service = CarService(db)
    return service.get_all_cars(skip=skip, limit=limit)


@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    """
    Endpoint para atualizar um carro existente
    """
    try:
        service = CarService(db)
        updated_car = service.update_car(
            car_id=car_id,
            brand=car.brand,
            model=car.model,
            year=car.year,
            color=car.color,
            plate=car.plate,
        )
        if not updated_car:
            raise HTTPException(status_code=404, detail="Carro não encontrado")
        return updated_car
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para deletar um carro
    """
    service = CarService(db)
    if not service.delete_car(car_id):
        raise HTTPException(status_code=404, detail="Carro não encontrado")
