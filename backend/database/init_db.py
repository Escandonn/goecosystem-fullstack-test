"""Inicialización de la base de datos."""

from database.base import Base
from database.session import engine
from models import patient, user  # noqa: F401  - Importa los modelos para registrarlos en Base


def init_db() -> None:
    """Crea todas las tablas definidas en los modelos en la base de datos."""
    Base.metadata.create_all(bind=engine)

    # Crear usuario admin inicial si no existe
    from core.config import settings
    from database.session import SessionLocal
    from services.user_service import UserService

    db = SessionLocal()
    try:
        service = UserService(db)
        service.ensure_admin_exists(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
        )
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("✅ Base de datos inicializada correctamente.")
