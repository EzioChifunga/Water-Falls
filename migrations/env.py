from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

# Carregar variáveis de ambiente
load_dotenv()

# Adiciona o caminho raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.infrastructure.config.database import Base  # IMPORTANTE
from app.infrastructure.models import (  # Importar todos os modelos
    CarModel,
    EnderecoModel,
    ClienteModel,
    CategoriaVeiculoModel,
    LojaModel,
    VeiculoModel,
    ReservaModel,
    PagamentoModel,
    HistoricoStatusVeiculoModel,
)

# Configuração Alembic
config = context.config

# Usar DATABASE_URL do .env se definido; caso contrário, construir a partir das partes
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    # Construir a URL do banco de dados a partir das variáveis de ambiente individuais
    DATABASE_URL = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    if os.getenv("DATABASE_SSLMODE") and os.getenv("DATABASE_SSLMODE") != "disable":
        DATABASE_URL += f"?sslmode={os.getenv('DATABASE_SSLMODE')}"

# Definir a URL no config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
print(f"[Alembic] Using DATABASE_URL: {DATABASE_URL}")  # Debug

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""  
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
