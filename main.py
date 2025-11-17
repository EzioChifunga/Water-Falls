"""
Entry point da aplicação FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.infrastructure.models import (
    CarModel, EnderecoModel, ClienteModel, CategoriaVeiculoModel,
    LojaModel, VeiculoModel, ReservaModel, PagamentoModel, HistoricoStatusVeiculoModel
)
from app.infrastructure.config.database import Base

# Importar rotas
from app.presentation.car_controller import router as car_router
from app.presentation.cliente_controller import router as cliente_router
from app.presentation.veiculo_controller import router as veiculo_router
from app.presentation.reserva_controller import router as reserva_router
from app.presentation.loja_controller import router as loja_router
from app.presentation.categoria_veiculo_controller import router as categoria_router
from app.presentation.endereco_controller import router as endereco_router
from app.presentation.pagamento_controller import router as pagamento_router
from app.presentation.historico_status_veiculo_controller import router as historico_router


# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(car_router)
app.include_router(cliente_router)
app.include_router(veiculo_router)
app.include_router(reserva_router)
app.include_router(loja_router)
app.include_router(categoria_router)
app.include_router(endereco_router)
app.include_router(pagamento_router)
app.include_router(historico_router)


@app.get("/")
def read_root():
    """Rota raiz da API"""
    return {
        "message": "Bem-vindo à WaterFalls API",
        "version": settings.api_version,
        "docs": "/docs",
        "endpoints": {
            "cars": "/cars",
            "clientes": "/clientes",
            "veiculos": "/veiculos",
            "reservas": "/reservas",
        }
    }


@app.get("/health")
def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
