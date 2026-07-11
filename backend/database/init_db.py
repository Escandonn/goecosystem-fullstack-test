"""Inicialización de la base de datos."""

from database.base import Base
from database.session import engine
from models import patient  # noqa: F401  - Importa el modelo para registrarlo en Base


def init_db() -> None:
    """Crea todas las tablas definidas en los modelos en la base de datos."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("✅ Base de datos inicializada correctamente.")
