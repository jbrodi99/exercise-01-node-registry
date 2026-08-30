"""
Database connection and session management.

Read DATABASE_URL from environment variable.
Create SQLAlchemy engine and session.
Provide a dependency for FastAPI to get a DB session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base 
import os

engine = create_engine(
    os.environ["DATABASE_URL"],
    pool_size=5,        # conexiones persistentes en el pool
    max_overflow=10,    # conexiones extra permitidas bajo carga
    pool_pre_ping=True, # valida la conexión antes de usarla (evita "server closed the connection")
    echo=False,         # True para debug: loguea el SQL generado
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()