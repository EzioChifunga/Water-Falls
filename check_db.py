#!/usr/bin/env python
"""Check database schema and status"""
from sqlalchemy import create_engine, inspect
from app.core.config import DATABASE_URL

print(f"Using DB: {DATABASE_URL}\n")
engine = create_engine(DATABASE_URL, future=True)
insp = inspect(engine)

# Check if veiculos table exists
if 'veiculos' in insp.get_table_names():
    print("✓ veiculos table EXISTS")
    cols = insp.get_columns('veiculos')
    print(f"\nColumns ({len(cols)}):")
    for c in cols:
        print(f"  - {c['name']}: {c['type']}")
    
    # Check for the new columns
    col_names = [c['name'] for c in cols]
    new_cols = ['cor', 'combustivel', 'portas', 'cambio', 'quilometragem']
    print(f"\nNew columns status:")
    for col in new_cols:
        status = "✓" if col in col_names else "✗"
        print(f"  {status} {col}")
else:
    print("✗ veiculos table NOT FOUND")

print("\nAll tables in DB:")
for tbl in insp.get_table_names():
    print(f"  - {tbl}")
