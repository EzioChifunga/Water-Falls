"""
Controlador para Histórico de Status de Veículo
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.historico_status_veiculo_service import HistoricoStatusVeiculoService
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schemas Pydantic
class HistoricoStatusVeiculoCreate(BaseModel):
    """Schema para criação de histórico"""
    veiculo_id: str
    status_anterior: Optional[str] = None
    status_atual: str


class HistoricoStatusVeiculoResponse(BaseModel):
    """Schema de resposta para histórico"""
    id: str
    veiculo_id: str
    status_anterior: Optional[str] = None
    status_atual: str
    data_mudanca: Optional[datetime] = None


# Router
router = APIRouter(
    prefix="/historico-status-veiculo",
    tags=["historico_status_veiculo"],
)


@router.post("/", response_model=HistoricoStatusVeiculoResponse, status_code=201)
def create_historico(historico: HistoricoStatusVeiculoCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de histórico"""
    service = HistoricoStatusVeiculoService(db)
    try:
        result = service.create_historico(
            veiculo_id=historico.veiculo_id,
            status_anterior=historico.status_anterior,
            status_atual=historico.status_atual,
        )
        return HistoricoStatusVeiculoResponse(
            id=result.id,
            veiculo_id=result.veiculo_id,
            status_anterior=result.status_anterior,
            status_atual=result.status_atual,
            data_mudanca=result.data_mudanca,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{historico_id}", response_model=HistoricoStatusVeiculoResponse)
def get_historico(historico_id: str, db: Session = Depends(get_db)):
    """Obtém um histórico pelo ID"""
    service = HistoricoStatusVeiculoService(db)
    historico = service.get_historico(historico_id)
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return HistoricoStatusVeiculoResponse(
        id=historico.id,
        veiculo_id=historico.veiculo_id,
        status_anterior=historico.status_anterior,
        status_atual=historico.status_atual,
        data_mudanca=historico.data_mudanca,
    )


@router.get("/veiculo/{veiculo_id}", response_model=List[HistoricoStatusVeiculoResponse])
def get_historicos_veiculo(veiculo_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtém todos os históricos de um veículo"""
    service = HistoricoStatusVeiculoService(db)
    historicos = service.get_historicos_veiculo(veiculo_id, skip, limit)
    return [
        HistoricoStatusVeiculoResponse(
            id=h.id,
            veiculo_id=h.veiculo_id,
            status_anterior=h.status_anterior,
            status_atual=h.status_atual,
            data_mudanca=h.data_mudanca,
        )
        for h in historicos
    ]


@router.get("/", response_model=List[HistoricoStatusVeiculoResponse])
def get_all_historicos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtém todos os históricos"""
    service = HistoricoStatusVeiculoService(db)
    historicos = service.get_all_historicos(skip, limit)
    return [
        HistoricoStatusVeiculoResponse(
            id=h.id,
            veiculo_id=h.veiculo_id,
            status_anterior=h.status_anterior,
            status_atual=h.status_atual,
            data_mudanca=h.data_mudanca,
        )
        for h in historicos
    ]
