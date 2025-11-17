"""
Controller/Rotas para gerenciar Veículos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.veiculo_service import VeiculoService


# Schemas
class VeiculoCreate(BaseModel):
    placa: str
    marca: str
    modelo: str
    ano: int
    categoria_id: str
    diaria: float
    loja_id: str
    latitude: float | None = None
    longitude: float | None = None
    cor: str | None = None
    combustivel: str | None = None
    portas: int | None = None
    cambio: str | None = None
    quilometragem: float | None = None


class VeiculoUpdate(BaseModel):
    placa: str
    marca: str
    modelo: str
    ano: int
    categoria_id: str
    diaria: float
    status: str
    loja_id: str
    latitude: float | None = None
    longitude: float | None = None
    cor: str | None = None
    combustivel: str | None = None
    portas: int | None = None
    cambio: str | None = None
    quilometragem: float | None = None


class VeiculoStatusUpdate(BaseModel):
    status: str


class VeiculoResponse(BaseModel):
    id: str
    placa: str
    marca: str
    modelo: str
    ano: int
    categoria_id: str
    diaria: float
    status: str
    loja_id: str
    latitude: float | None
    longitude: float | None
    cor: str | None
    combustivel: str | None
    portas: int | None
    cambio: str | None
    quilometragem: float | None
    
    class Config:
        from_attributes = True


router = APIRouter(prefix="/veiculos", tags=["veiculos"])


@router.post("/", response_model=VeiculoResponse, status_code=201)
def create_veiculo(veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    """Criar um novo veículo"""
    try:
        service = VeiculoService(db)
        created = service.create_veiculo(
            placa=veiculo.placa,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
            categoria_id=veiculo.categoria_id,
            diaria=veiculo.diaria,
            loja_id=veiculo.loja_id,
            latitude=veiculo.latitude,
            longitude=veiculo.longitude,
            cor=veiculo.cor,
            combustivel=veiculo.combustivel,
            portas=veiculo.portas,
            cambio=veiculo.cambio,
            quilometragem=veiculo.quilometragem,
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/placa/{placa}", response_model=VeiculoResponse)
def get_veiculo_by_placa(placa: str, db: Session = Depends(get_db)):
    """Obter um veículo pela placa"""
    service = VeiculoService(db)
    veiculo = service.get_veiculo_by_placa(placa)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.get("/{veiculo_id}", response_model=VeiculoResponse)
def get_veiculo(veiculo_id: str, db: Session = Depends(get_db)):
    """Obter um veículo pelo ID"""
    service = VeiculoService(db)
    veiculo = service.get_veiculo(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.get("/loja/{loja_id}", response_model=List[VeiculoResponse])
def get_veiculos_loja(
    loja_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter veículos de uma loja"""
    service = VeiculoService(db)
    return service.get_veiculos_by_loja(loja_id, skip=skip, limit=limit)


@router.get("/disponveis", response_model=List[VeiculoResponse])
def get_veiculos_disponiveis(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter veículos disponíveis"""
    service = VeiculoService(db)
    return service.get_veiculos_disponiveis(skip=skip, limit=limit)


@router.get("/", response_model=List[VeiculoResponse])
def get_all_veiculos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter todos os veículos"""
    service = VeiculoService(db)
    return service.get_all_veiculos(skip=skip, limit=limit)


@router.put("/{veiculo_id}", response_model=VeiculoResponse)
def update_veiculo(veiculo_id: str, veiculo: VeiculoUpdate, db: Session = Depends(get_db)):
    """Atualizar um veículo"""
    try:
        service = VeiculoService(db)
        updated = service.update_veiculo(
            veiculo_id=veiculo_id,
            placa=veiculo.placa,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
            categoria_id=veiculo.categoria_id,
            diaria=veiculo.diaria,
            status=veiculo.status,
            loja_id=veiculo.loja_id,
            latitude=veiculo.latitude,
            longitude=veiculo.longitude,
            cor=veiculo.cor,
            combustivel=veiculo.combustivel,
            portas=veiculo.portas,
            cambio=veiculo.cambio,
            quilometragem=veiculo.quilometragem,
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{veiculo_id}/status", response_model=VeiculoResponse)
def update_veiculo_status(veiculo_id: str, status_update: VeiculoStatusUpdate, db: Session = Depends(get_db)):
    """Atualizar apenas o status de um veículo"""
    service = VeiculoService(db)
    updated = service.update_status(veiculo_id, status_update.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return updated


@router.delete("/{veiculo_id}", status_code=204)
def delete_veiculo(veiculo_id: str, db: Session = Depends(get_db)):
    """Deletar um veículo"""
    service = VeiculoService(db)
    if not service.delete_veiculo(veiculo_id):
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
