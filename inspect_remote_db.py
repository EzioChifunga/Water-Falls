"""
Script para inspecionar o banco de dados remoto
"""
from sqlalchemy import create_engine, inspect
from app.infrastructure.config.database import DATABASE_URL

print(f"Conectando ao banco: {DATABASE_URL}\n")

engine = create_engine(DATABASE_URL, echo=False)

inspector = inspect(engine)

# Listar todas as tabelas
tables = inspector.get_table_names()
print(f"Tabelas no banco ({len(tables)}):")
for table in sorted(tables):
    print(f"  - {table}")

print("\n" + "="*80 + "\n")

# Inspecionar colunas de cada tabela
for table in sorted(tables):
    columns = inspector.get_columns(table)
    print(f"Tabela: {table}")
    for col in columns:
        col_type = str(col['type'])
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        print(f"  - {col['name']}: {col_type} {nullable}")
    print()
