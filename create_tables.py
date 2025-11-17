#!/usr/bin/env python
"""Create all tables from SQLAlchemy metadata"""
from sqlalchemy import create_engine, inspect
from app.infrastructure.config.database import Base, DATABASE_URL

# Get the database URL
print(f"Creating tables in: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=False)

# Create all tables
Base.metadata.create_all(bind=engine)
print("✓ All tables created successfully!")

# List created tables
insp = inspect(engine)
tables = insp.get_table_names()
print(f"\nTables in database ({len(tables)}):")
for tbl in tables:
    print(f"  - {tbl}")
