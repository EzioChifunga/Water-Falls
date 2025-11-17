"""
Controller/Rotas para gerenciar Reservas
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.reserva_service import ReservaService


# Schemas
class ReservaCreate(BaseModel):
    cliente_id: str
    veiculo_id: str
    loja_retirada_id: str
    loja_devolucao_id: str
    data_inicio: date
    data_fim: date
    periodo: int  # 7, 15, 30
    valor_total: float
    motorista_incluido: bool = False
    canal_origem: str = "WEB"


class ReservaUpdate(BaseModel):
    cliente_id: str
    veiculo_id: str
    loja_retirada_id: str
    loja_devolucao_id: str
    data_inicio: date
    data_fim: date
    periodo: int
    valor_total: float
    motorista_incluido: bool
    canal_origem: str
    status: str


class ReservaResponse(BaseModel):
    id: str
    cliente_id: str
    veiculo_id: str
    loja_retirada_id: str
    loja_devolucao_id: str
    data_inicio: date
    data_fim: date
    periodo: int
    valor_total: float
    motorista_incluido: bool
    canal_origem: str
    status: str
    
    class Config:
        from_attributes = True


router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post("/", response_model=ReservaResponse, status_code=201)
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Criar uma nova reserva"""
    try:
        service = ReservaService(db)
        created = service.create_reserva(
            cliente_id=reserva.cliente_id,
            veiculo_id=reserva.veiculo_id,
            loja_retirada_id=reserva.loja_retirada_id,
            loja_devolucao_id=reserva.loja_devolucao_id,
            data_inicio=reserva.data_inicio,
            data_fim=reserva.data_fim,
            periodo=reserva.periodo,
            valor_total=reserva.valor_total,
            motorista_incluido=reserva.motorista_incluido,
            canal_origem=reserva.canal_origem,
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{reserva_id}", response_model=ReservaResponse)
def get_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Obter uma reserva pelo ID"""
    service = ReservaService(db)
    reserva = service.get_reserva(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.get("/cliente/{cliente_id}", response_model=List[ReservaResponse])
def get_reservas_cliente(
    cliente_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter reservas de um cliente"""
    service = ReservaService(db)
    return service.get_reservas_cliente(cliente_id, skip=skip, limit=limit)


@router.get("/veiculo/{veiculo_id}", response_model=List[ReservaResponse])
def get_reservas_veiculo(
    veiculo_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter reservas de um veículo"""
    service = ReservaService(db)
    return service.get_reservas_veiculo(veiculo_id, skip=skip, limit=limit)


@router.get("/", response_model=List[ReservaResponse])
def get_all_reservas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter todas as reservas"""
    service = ReservaService(db)
    return service.get_all_reservas(skip=skip, limit=limit)


@router.patch("/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Confirmar uma reserva"""
    service = ReservaService(db)
    updated = service.confirmar_reserva(reserva_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return updated


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Cancelar uma reserva"""
    service = ReservaService(db)
    updated = service.cancelar_reserva(reserva_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return updated


@router.delete("/{reserva_id}", status_code=204)
def delete_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Deletar uma reserva"""
    service = ReservaService(db)
    if not service.delete_reserva(reserva_id):
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
