"""
Modelos ORM da aplicação
"""
from app.infrastructure.models.car_model import CarModel
from app.infrastructure.models.endereco_model import EnderecoModel
from app.infrastructure.models.cliente_model import ClienteModel
from app.infrastructure.models.categoria_veiculo_model import CategoriaVeiculoModel
from app.infrastructure.models.loja_model import LojaModel
from app.infrastructure.models.veiculo_model import VeiculoModel
from app.infrastructure.models.reserva_model import ReservaModel
from app.infrastructure.models.pagamento_model import PagamentoModel
from app.infrastructure.models.historico_status_veiculo_model import HistoricoStatusVeiculoModel

__all__ = [
    "CarModel",
    "EnderecoModel",
    "ClienteModel",
    "CategoriaVeiculoModel",
    "LojaModel",
    "VeiculoModel",
    "ReservaModel",
    "PagamentoModel",
    "HistoricoStatusVeiculoModel",
]
