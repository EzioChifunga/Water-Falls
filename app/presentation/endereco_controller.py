"""
Controlador para Endereços
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.endereco_service import EnderecoService
from pydantic import BaseModel, field_validator


# Schemas Pydantic
class EnderecoCreate(BaseModel):
    """Schema para criação de endereço"""
    rua: str
    cidade: str
    estado: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("Estado deve ser uma sigla com exatamente 2 caracteres (ex: SP, RJ, MG)")
        return v.upper()


class EnderecoUpdate(BaseModel):
    """Schema para atualização de endereço"""
    rua: str
    cidade: str
    estado: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("Estado deve ser uma sigla com exatamente 2 caracteres (ex: SP, RJ, MG)")
        return v.upper()


class EnderecoResponse(BaseModel):
    """Schema de resposta para endereço"""
    id: str
    rua: str
    cidade: str
    estado: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# Router
router = APIRouter(
    prefix="/enderecos",
    tags=["enderecos"],
)


@router.post("/", response_model=EnderecoResponse, status_code=201)
def create_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    """Cria um novo endereço"""
    service = EnderecoService(db)
    try:
        result = service.create_endereco(
            rua=endereco.rua,
            cidade=endereco.cidade,
            estado=endereco.estado,
            latitude=endereco.latitude,
            longitude=endereco.longitude,
        )
        return EnderecoResponse(
            id=result.id,
            rua=result.rua,
            cidade=result.cidade,
            estado=result.estado,
            latitude=result.latitude,
            longitude=result.longitude,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{endereco_id}", response_model=EnderecoResponse)
def get_endereco(endereco_id: str, db: Session = Depends(get_db)):
    """Obtém um endereço pelo ID"""
    service = EnderecoService(db)
    endereco = service.get_endereco(endereco_id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return EnderecoResponse(
        id=endereco.id,
        rua=endereco.rua,
        cidade=endereco.cidade,
        estado=endereco.estado,
        latitude=endereco.latitude,
        longitude=endereco.longitude,
    )


@router.get("/", response_model=List[EnderecoResponse])
def get_all_enderecos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtém todos os endereços"""
    service = EnderecoService(db)
    enderecos = service.get_all_enderecos(skip, limit)
    return [
        EnderecoResponse(
            id=e.id,
            rua=e.rua,
            cidade=e.cidade,
            estado=e.estado,
            latitude=e.latitude,
            longitude=e.longitude,
        )
        for e in enderecos
    ]


@router.put("/{endereco_id}", response_model=EnderecoResponse)
def update_endereco(endereco_id: str, endereco: EnderecoUpdate, db: Session = Depends(get_db)):
    """Atualiza um endereço"""
    service = EnderecoService(db)
    try:
        result = service.update_endereco(
            endereco_id=endereco_id,
            rua=endereco.rua,
            cidade=endereco.cidade,
            estado=endereco.estado,
            latitude=endereco.latitude,
            longitude=endereco.longitude,
        )
        if not result:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
        return EnderecoResponse(
            id=result.id,
            rua=result.rua,
            cidade=result.cidade,
            estado=result.estado,
            latitude=result.latitude,
            longitude=result.longitude,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{endereco_id}", status_code=204)
def delete_endereco(endereco_id: str, db: Session = Depends(get_db)):
    """Deleta um endereço"""
    service = EnderecoService(db)
    if not service.delete_endereco(endereco_id):
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return None
