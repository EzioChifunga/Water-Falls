"""
Controlador para Categorias de Veículos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.categoria_veiculo_service import CategoriaVeiculoService
from pydantic import BaseModel


# Schemas Pydantic
class CategoriaVeiculoCreate(BaseModel):
    """Schema para criação de categoria"""
    nome: str


class CategoriaVeiculoUpdate(BaseModel):
    """Schema para atualização de categoria"""
    nome: str


class CategoriaVeiculoResponse(BaseModel):
    """Schema de resposta para categoria"""
    id: str
    nome: str


# Router
router = APIRouter(
    prefix="/categorias",
    tags=["categorias_veiculos"],
)


@router.post("/", response_model=CategoriaVeiculoResponse, status_code=201)
def create_categoria(categoria: CategoriaVeiculoCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria de veículo"""
    service = CategoriaVeiculoService(db)
    try:
        result = service.create_categoria(nome=categoria.nome)
        return CategoriaVeiculoResponse(
            id=result.id,
            nome=result.nome,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{categoria_id}", response_model=CategoriaVeiculoResponse)
def get_categoria(categoria_id: str, db: Session = Depends(get_db)):
    """Obtém uma categoria pelo ID"""
    service = CategoriaVeiculoService(db)
    categoria = service.get_categoria(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return CategoriaVeiculoResponse(
        id=categoria.id,
        nome=categoria.nome,
    )


@router.get("/", response_model=List[CategoriaVeiculoResponse])
def get_all_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtém todas as categorias de veículos"""
    service = CategoriaVeiculoService(db)
    categorias = service.get_all_categorias(skip, limit)
    return [
        CategoriaVeiculoResponse(
            id=categoria.id,
            nome=categoria.nome,
        )
        for categoria in categorias
    ]


@router.put("/{categoria_id}", response_model=CategoriaVeiculoResponse)
def update_categoria(categoria_id: str, categoria: CategoriaVeiculoUpdate, db: Session = Depends(get_db)):
    """Atualiza uma categoria"""
    service = CategoriaVeiculoService(db)
    try:
        result = service.update_categoria(
            categoria_id=categoria_id,
            nome=categoria.nome,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return CategoriaVeiculoResponse(
            id=result.id,
            nome=result.nome,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{categoria_id}", status_code=204)
def delete_categoria(categoria_id: str, db: Session = Depends(get_db)):
    """Deleta uma categoria"""
    service = CategoriaVeiculoService(db)
    if not service.delete_categoria(categoria_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return None
