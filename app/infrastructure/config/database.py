# app/infrastructure/config/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Prefer DATABASE_URL if defined, otherwise build from parts
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    DATABASE_URL = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    if os.getenv("DATABASE_SSLMODE") and os.getenv("DATABASE_SSLMODE") != "disable":
        DATABASE_URL += f"?sslmode={os.getenv('DATABASE_SSLMODE')}"

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base central usada em toda a aplicação
Base = declarative_base()
