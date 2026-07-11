"""Configuración de la sesión de base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings

# Engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False,
)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependencia que proporciona una sesión de base de datos por request."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
