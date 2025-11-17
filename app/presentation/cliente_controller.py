"""
Controller/Rotas para gerenciar Clientes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.cliente_service import ClienteService


# Schemas
class EnderecoCreate(BaseModel):
    rua: str
    cidade: str
    estado: str
    latitude: float | None = None
    longitude: float | None = None


class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    cnh_numero: str
    cnh_validade: str  # YYYY-MM-DD
    telefone: str | None = None
    email: str | None = None
    endereco_id: str | None = None


class ClienteUpdate(BaseModel):
    nome: str
    cpf: str
    cnh_numero: str
    cnh_validade: str
    telefone: str | None = None
    email: str | None = None
    endereco_id: str | None = None


class ClienteResponse(BaseModel):
    id: str
    nome: str
    cpf: str
    telefone: str | None
    email: str | None
    endereco_id: str | None
    cnh_numero: str
    cnh_validade: str
    
    class Config:
        from_attributes = True


router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=201)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Criar um novo cliente"""
    try:
        service = ClienteService(db)
        created = service.create_cliente(
            nome=cliente.nome,
            cpf=cliente.cpf,
            cnh_numero=cliente.cnh_numero,
            cnh_validade=cliente.cnh_validade,
            telefone=cliente.telefone,
            email=cliente.email,
            endereco_id=cliente.endereco_id,
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Obter um cliente pelo ID"""
    service = ClienteService(db)
    cliente = service.get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.get("/", response_model=List[ClienteResponse])
def get_all_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter todos os clientes"""
    service = ClienteService(db)
    return service.get_all_clientes(skip=skip, limit=limit)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(cliente_id: str, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    """Atualizar um cliente"""
    try:
        service = ClienteService(db)
        updated = service.update_cliente(
            cliente_id=cliente_id,
            nome=cliente.nome,
            cpf=cliente.cpf,
            cnh_numero=cliente.cnh_numero,
            cnh_validade=cliente.cnh_validade,
            telefone=cliente.telefone,
            email=cliente.email,
            endereco_id=cliente.endereco_id,
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Deletar um cliente"""
    service = ClienteService(db)
    if not service.delete_cliente(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
