"""
Controlador para Pagamentos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.pagamento_service import PagamentoService
from pydantic import BaseModel
from datetime import datetime


# Schemas Pydantic
class PagamentoCreate(BaseModel):
    """Schema para criação de pagamento"""
    reserva_id: str
    metodo: str
    status: str
    valor: float
    transacao_gateway_id: Optional[str] = None


class PagamentoUpdate(BaseModel):
    """Schema para atualização de pagamento"""
    metodo: str
    status: str
    valor: float
    transacao_gateway_id: Optional[str] = None


class PagamentoResponse(BaseModel):
    """Schema de resposta para pagamento"""
    id: str
    reserva_id: str
    metodo: str
    status: str
    valor: float
    transacao_gateway_id: Optional[str] = None
    criado_em: Optional[datetime] = None


# Router
router = APIRouter(
    prefix="/pagamentos",
    tags=["pagamentos"],
)


@router.post("/", response_model=PagamentoResponse, status_code=201)
def create_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    """Cria um novo pagamento"""
    service = PagamentoService(db)
    try:
        result = service.create_pagamento(
            reserva_id=pagamento.reserva_id,
            metodo=pagamento.metodo,
            status=pagamento.status,
            valor=pagamento.valor,
            transacao_gateway_id=pagamento.transacao_gateway_id,
        )
        return PagamentoResponse(
            id=result.id,
            reserva_id=result.reserva_id,
            metodo=result.metodo,
            status=result.status,
            valor=result.valor,
            transacao_gateway_id=result.transacao_gateway_id,
            criado_em=result.criado_em,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def get_pagamento(pagamento_id: str, db: Session = Depends(get_db)):
    """Obtém um pagamento pelo ID"""
    service = PagamentoService(db)
    pagamento = service.get_pagamento(pagamento_id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return PagamentoResponse(
        id=pagamento.id,
        reserva_id=pagamento.reserva_id,
        metodo=pagamento.metodo,
        status=pagamento.status,
        valor=pagamento.valor,
        transacao_gateway_id=pagamento.transacao_gateway_id,
        criado_em=pagamento.criado_em,
    )


@router.get("/reserva/{reserva_id}", response_model=PagamentoResponse)
def get_pagamento_by_reserva(reserva_id: str, db: Session = Depends(get_db)):
    """Obtém um pagamento pela reserva"""
    service = PagamentoService(db)
    pagamento = service.get_pagamento_by_reserva(reserva_id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return PagamentoResponse(
        id=pagamento.id,
        reserva_id=pagamento.reserva_id,
        metodo=pagamento.metodo,
        status=pagamento.status,
        valor=pagamento.valor,
        transacao_gateway_id=pagamento.transacao_gateway_id,
        criado_em=pagamento.criado_em,
    )


@router.get("/", response_model=List[PagamentoResponse])
def get_all_pagamentos(skip: int = 0, limit: int = 100, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Obtém todos os pagamentos (ou filtra por status)"""
    service = PagamentoService(db)
    if status:
        pagamentos = service.get_pagamentos_by_status(status, skip, limit)
    else:
        pagamentos = service.get_all_pagamentos(skip, limit)
    return [
        PagamentoResponse(
            id=p.id,
            reserva_id=p.reserva_id,
            metodo=p.metodo,
            status=p.status,
            valor=p.valor,
            transacao_gateway_id=p.transacao_gateway_id,
            criado_em=p.criado_em,
        )
        for p in pagamentos
    ]


@router.put("/{pagamento_id}", response_model=PagamentoResponse)
def update_pagamento(pagamento_id: str, pagamento: PagamentoUpdate, db: Session = Depends(get_db)):
    """Atualiza um pagamento"""
    service = PagamentoService(db)
    try:
        result = service.update_pagamento(
            pagamento_id=pagamento_id,
            metodo=pagamento.metodo,
            status=pagamento.status,
            valor=pagamento.valor,
            transacao_gateway_id=pagamento.transacao_gateway_id,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return PagamentoResponse(
            id=result.id,
            reserva_id=result.reserva_id,
            metodo=result.metodo,
            status=result.status,
            valor=result.valor,
            transacao_gateway_id=result.transacao_gateway_id,
            criado_em=result.criado_em,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{pagamento_id}", status_code=204)
def delete_pagamento(pagamento_id: str, db: Session = Depends(get_db)):
    """Deleta um pagamento"""
    service = PagamentoService(db)
    if not service.delete_pagamento(pagamento_id):
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return None
