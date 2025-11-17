"""
Serviço de aplicação para gerenciar Veículos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.veiculos import Veiculo, CategoriaVeiculo
from app.infrastructure.repositories.veiculo_repository import VeiculoRepository
from app.infrastructure.repositories.categoria_veiculo_repository import CategoriaVeiculoRepository


class VeiculoService:
    """Serviço de aplicação para operações com veículos"""
    
    def __init__(self, db: Session):
        self.veiculo_repo = VeiculoRepository(db)
        self.categoria_repo = CategoriaVeiculoRepository(db)
    
    def create_veiculo(self, placa: str, marca: str, modelo: str, ano: int, 
                      categoria_id: str, diaria: float, loja_id: str,
                      quantidade: int = 1,
                      cor: Optional[str] = None,
                      combustivel: Optional[str] = None,
                      portas: Optional[int] = None,
                      cambio: Optional[str] = None,
                      quilometragem: Optional[float] = None,
                      image_url: Optional[str] = None,
                      latitude: Optional[float] = None, longitude: Optional[float] = None) -> Veiculo:
        """Criar um novo veículo e adicionar ao estoque de uma loja"""
        # Validar se placa já existe
        existing_placa = self.veiculo_repo.get_by_placa(placa)
        if existing_placa:
            raise ValueError(f"Já existe um veículo com a placa {placa}")
        # Validar se categoria existe
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            raise ValueError(f"Categoria {categoria_id} não encontrada")
        veiculo = Veiculo(
            placa=placa,
            marca=marca,
            modelo=modelo,
            image_url=image_url,
            ano=ano,
            cor=cor,
            combustivel=combustivel,
            portas=portas,
            cambio=cambio,
            quilometragem=quilometragem,
            categoria_id=categoria_id,
            diaria=diaria,
            status="DISPONIVEL",
            latitude=latitude,
            longitude=longitude,
        )
        return self.veiculo_repo.create(veiculo, loja_id=loja_id, quantidade=quantidade)
    
    def get_veiculo(self, veiculo_id: str) -> Optional[Veiculo]:
        """Obter um veículo pelo ID"""
        return self.veiculo_repo.get_by_id(veiculo_id)
    
    def get_veiculo_by_placa(self, placa: str) -> Optional[Veiculo]:
        """Obter um veículo pela placa"""
        return self.veiculo_repo.get_by_placa(placa)
    
    def get_veiculos_disponiveis(self, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obter veículos disponíveis"""
        return self.veiculo_repo.get_by_status("DISPONIVEL", skip=skip, limit=limit)
    
    def get_veiculos_by_loja(self, loja_id: str, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obter veículos de uma loja"""
        return self.veiculo_repo.get_by_loja(loja_id, skip=skip, limit=limit)
    
    def get_all_veiculos(self, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """Obter todos os veículos"""
        return self.veiculo_repo.get_all(skip=skip, limit=limit)
    
    def update_veiculo(self, veiculo_id: str, placa: str, marca: str, modelo: str, 
                       ano: int, categoria_id: str, diaria: float, status: str,
                       cor: Optional[str] = None,
                       combustivel: Optional[str] = None,
                       portas: Optional[int] = None,
                       cambio: Optional[str] = None,
                       quilometragem: Optional[float] = None,
                       image_url: Optional[str] = None,
                       latitude: Optional[float] = None, 
                       longitude: Optional[float] = None) -> Optional[Veiculo]:
        """Atualizar um veículo (sem loja_id)"""
        existing = self.veiculo_repo.get_by_id(veiculo_id)
        if not existing:
            return None
        # Validar se placa já existe em outro veículo
        if placa != existing.placa:
            existing_placa = self.veiculo_repo.get_by_placa(placa)
            if existing_placa:
                raise ValueError(f"Já existe outro veículo com a placa {placa}")
        # Validar categoria
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            raise ValueError(f"Categoria {categoria_id} não encontrada")
        veiculo = Veiculo(
            placa=placa,
            marca=marca,
            image_url=image_url,
            modelo=modelo,
            ano=ano,
            cor=cor,
            combustivel=combustivel,
            portas=portas,
            cambio=cambio,
            quilometragem=quilometragem,
            categoria_id=categoria_id,
            diaria=diaria,
            status=status,
            latitude=latitude,
            longitude=longitude,
        )
        return self.veiculo_repo.update(veiculo_id, veiculo)
    
    def update_status(self, veiculo_id: str, novo_status: str) -> Optional[Veiculo]:
        """Atualizar apenas o status de um veículo"""
        existing = self.veiculo_repo.get_by_id(veiculo_id)
        if not existing:
            return None
        
        existing.status = novo_status
        return self.veiculo_repo.update(veiculo_id, existing)
    
    def delete_veiculo(self, veiculo_id: str) -> bool:
        """Deletar um veículo"""
        return self.veiculo_repo.delete(veiculo_id)
