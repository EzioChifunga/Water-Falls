"""
Controlador para Lojas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.loja_service import LojaService
from pydantic import BaseModel


# Schemas Pydantic
class LojaCreate(BaseModel):
    """Schema para criação de loja"""
    nome: str
    telefone: str
    endereco_id: str


class LojaUpdate(BaseModel):
    """Schema para atualização de loja"""
    nome: str
    telefone: str
    endereco_id: str


class LojaResponse(BaseModel):
    """Schema de resposta para loja"""
    id: str
    nome: str
    telefone: str
    endereco_id: str


# Router
router = APIRouter(
    prefix="/lojas",
    tags=["lojas"],
)


@router.post("/", response_model=LojaResponse, status_code=201)
def create_loja(loja: LojaCreate, db: Session = Depends(get_db)):
    """Cria uma nova loja"""
    service = LojaService(db)
    try:
        result = service.create_loja(
            nome=loja.nome,
            telefone=loja.telefone,
            endereco_id=loja.endereco_id,
        )
        return LojaResponse(
            id=result.id,
            nome=result.nome,
            telefone=result.telefone,
            endereco_id=result.endereco_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{loja_id}", response_model=LojaResponse)
def get_loja(loja_id: str, db: Session = Depends(get_db)):
    """Obtém uma loja pelo ID"""
    service = LojaService(db)
    loja = service.get_loja(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return LojaResponse(
        id=loja.id,
        nome=loja.nome,
        telefone=loja.telefone,
        endereco_id=loja.endereco_id,
    )


@router.get("/", response_model=List[LojaResponse])
def get_all_lojas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtém todas as lojas"""
    service = LojaService(db)
    lojas = service.get_all_lojas(skip, limit)
    return [
        LojaResponse(
            id=loja.id,
            nome=loja.nome,
            telefone=loja.telefone,
            endereco_id=loja.endereco_id,
        )
        for loja in lojas
    ]


@router.put("/{loja_id}", response_model=LojaResponse)
def update_loja(loja_id: str, loja: LojaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma loja"""
    service = LojaService(db)
    try:
        result = service.update_loja(
            loja_id=loja_id,
            nome=loja.nome,
            telefone=loja.telefone,
            endereco_id=loja.endereco_id,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        return LojaResponse(
            id=result.id,
            nome=result.nome,
            telefone=result.telefone,
            endereco_id=result.endereco_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{loja_id}", status_code=204)
def delete_loja(loja_id: str, db: Session = Depends(get_db)):
    """Deleta uma loja"""
    service = LojaService(db)
    if not service.delete_loja(loja_id):
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return None
