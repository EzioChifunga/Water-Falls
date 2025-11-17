"""
Controller/Rotas para gerenciar Estoque de Veículos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.models.estoque_veiculo_model import EstoqueVeiculoModel
from app.infrastructure.models.veiculo_model import VeiculoModel
from app.infrastructure.models.loja_model import LojaModel

import uuid


class EstoqueCreate(BaseModel):
    veiculo_id: str
    loja_id: str
    quantidade: int = Field(..., ge=1)
    status: Optional[str] = "DISPONIVEL"


class EstoqueUpdate(BaseModel):
    quantidade: Optional[int] = Field(None, ge=0)
    status: Optional[str]


class EstoqueTransfer(BaseModel):
    veiculo_id: str
    from_loja_id: str
    to_loja_id: str
    quantidade: int = Field(..., ge=1)


class EstoqueResponse(BaseModel):
    id: str
    veiculo_id: str
    loja_id: str
    quantidade: int
    status: str
    criado_em: Optional[str] = None
    atualizado_em: Optional[str] = None

    class Config:
        from_attributes = True


router = APIRouter(prefix="/estoque", tags=["estoque"])


def _uuid_or_400(value: str, name: str):
    try:
        return uuid.UUID(str(value))
    except Exception:
        raise HTTPException(status_code=400, detail=f"{name} inválido")


@router.post("/", response_model=EstoqueResponse, status_code=201)
def create_estoque(body: EstoqueCreate, db: Session = Depends(get_db)):
    """Criar ou incrementar entrada de estoque para um veículo em uma loja"""
    veiculo_id = _uuid_or_400(body.veiculo_id, "veiculo_id")
    loja_id = _uuid_or_400(body.loja_id, "loja_id")

    # validar existência de veículo e loja
    veiculo = db.query(VeiculoModel).filter(VeiculoModel.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    loja = db.query(LojaModel).filter(LojaModel.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")

    # se já existe estoque, incrementar
    estoque = db.query(EstoqueVeiculoModel).filter(
        EstoqueVeiculoModel.veiculo_id == veiculo_id,
        EstoqueVeiculoModel.loja_id == loja_id
    ).first()
    if estoque:
        estoque.quantidade = estoque.quantidade + body.quantidade
        if body.status:
            estoque.status = body.status
        db.commit()
        db.refresh(estoque)
        return EstoqueResponse(
            id=str(estoque.id),
            veiculo_id=str(estoque.veiculo_id),
            loja_id=str(estoque.loja_id),
            quantidade=estoque.quantidade,
            status=estoque.status,
            criado_em=str(estoque.criado_em),
            atualizado_em=str(estoque.atualizado_em),
        )

    novo = EstoqueVeiculoModel(
        veiculo_id=veiculo_id,
        loja_id=loja_id,
        quantidade=body.quantidade,
        status=body.status or "DISPONIVEL",
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return EstoqueResponse(
        id=str(novo.id),
        veiculo_id=str(novo.veiculo_id),
        loja_id=str(novo.loja_id),
        quantidade=novo.quantidade,
        status=novo.status,
        criado_em=str(novo.criado_em),
        atualizado_em=str(novo.atualizado_em),
    )


@router.get("/loja/{loja_id}", response_model=List[EstoqueResponse])
def get_by_loja(loja_id: str, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    _id = _uuid_or_400(loja_id, "loja_id")
    itens = db.query(EstoqueVeiculoModel).filter(EstoqueVeiculoModel.loja_id == _id).offset(skip).limit(limit).all()
    return [
        EstoqueResponse(
            id=str(i.id),
            veiculo_id=str(i.veiculo_id),
            loja_id=str(i.loja_id),
            quantidade=i.quantidade,
            status=i.status,
            criado_em=str(i.criado_em),
            atualizado_em=str(i.atualizado_em),
        ) for i in itens
    ]


@router.get("/veiculo/{veiculo_id}", response_model=List[EstoqueResponse])
def get_by_veiculo(veiculo_id: str, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    _id = _uuid_or_400(veiculo_id, "veiculo_id")
    itens = db.query(EstoqueVeiculoModel).filter(EstoqueVeiculoModel.veiculo_id == _id).offset(skip).limit(limit).all()
    return [
        EstoqueResponse(
            id=str(i.id),
            veiculo_id=str(i.veiculo_id),
            loja_id=str(i.loja_id),
            quantidade=i.quantidade,
            status=i.status,
            criado_em=str(i.criado_em),
            atualizado_em=str(i.atualizado_em),
        ) for i in itens
    ]


@router.put("/{estoque_id}", response_model=EstoqueResponse)
def update_estoque(estoque_id: str, body: EstoqueUpdate, db: Session = Depends(get_db)):
    _id = _uuid_or_400(estoque_id, "estoque_id")
    est = db.query(EstoqueVeiculoModel).filter(EstoqueVeiculoModel.id == _id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    if body.quantidade is not None:
        est.quantidade = body.quantidade
    if body.status is not None:
        est.status = body.status
    db.commit()
    db.refresh(est)
    return EstoqueResponse(
        id=str(est.id),
        veiculo_id=str(est.veiculo_id),
        loja_id=str(est.loja_id),
        quantidade=est.quantidade,
        status=est.status,
        criado_em=str(est.criado_em),
        atualizado_em=str(est.atualizado_em),
    )


@router.post("/transfer", response_model=List[EstoqueResponse])
def transfer_estoque(body: EstoqueTransfer, db: Session = Depends(get_db)):
    """Transferir quantidade de um veículo entre lojas (decrementa origem, incrementa destino)."""
    veiculo_id = _uuid_or_400(body.veiculo_id, "veiculo_id")
    from_id = _uuid_or_400(body.from_loja_id, "from_loja_id")
    to_id = _uuid_or_400(body.to_loja_id, "to_loja_id")
    if from_id == to_id:
        raise HTTPException(status_code=400, detail="Loja de origem e destino devem ser diferentes")

    origem = db.query(EstoqueVeiculoModel).filter(
        EstoqueVeiculoModel.veiculo_id == veiculo_id,
        EstoqueVeiculoModel.loja_id == from_id
    ).with_for_update().first()
    if not origem or origem.quantidade < body.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente na loja de origem")

    destino = db.query(EstoqueVeiculoModel).filter(
        EstoqueVeiculoModel.veiculo_id == veiculo_id,
        EstoqueVeiculoModel.loja_id == to_id
    ).with_for_update().first()

    origem.quantidade = origem.quantidade - body.quantidade
    if origem.quantidade < 0:
        raise HTTPException(status_code=400, detail="Quantidade resultaria negativa")

    if destino:
        destino.quantidade = destino.quantidade + body.quantidade
    else:
        destino = EstoqueVeiculoModel(
            veiculo_id=veiculo_id,
            loja_id=to_id,
            quantidade=body.quantidade,
            status=origem.status,
        )
        db.add(destino)

    db.commit()
    db.refresh(origem)
    db.refresh(destino)

    return [
        EstoqueResponse(
            id=str(origem.id),
            veiculo_id=str(origem.veiculo_id),
            loja_id=str(origem.loja_id),
            quantidade=origem.quantidade,
            status=origem.status,
            criado_em=str(origem.criado_em),
            atualizado_em=str(origem.atualizado_em),
        ),
        EstoqueResponse(
            id=str(destino.id),
            veiculo_id=str(destino.veiculo_id),
            loja_id=str(destino.loja_id),
            quantidade=destino.quantidade,
            status=destino.status,
            criado_em=str(destino.criado_em),
            atualizado_em=str(destino.atualizado_em),
        )
    ]


@router.delete("/{estoque_id}", status_code=204)
def delete_estoque(estoque_id: str, db: Session = Depends(get_db)):
    _id = _uuid_or_400(estoque_id, "estoque_id")
    est = db.query(EstoqueVeiculoModel).filter(EstoqueVeiculoModel.id == _id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    db.delete(est)
    db.commit()
