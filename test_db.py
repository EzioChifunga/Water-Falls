import os
import sys
from sqlalchemy import text

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.infrastructure.config.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]
        print("Conectado ao banco:", db_name)
except Exception as e:
    print("Erro:", e)
