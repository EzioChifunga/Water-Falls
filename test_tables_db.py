from app.infrastructure.config.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tabelas existentes:", tables)
    