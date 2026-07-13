"""Configuración centralizada de la aplicación mediante variables de entorno."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """
    Clase de configuración centralizada de la aplicación.

    Toda la configuración se lee desde variables de entorno (.env),
    con valores por defecto para desarrollo.
    """

    # ── Aplicación ──────────────────────────────────────────────
    APP_NAME: str = os.getenv("APP_NAME", "GoEcosystem API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # ── Base de datos ───────────────────────────────────────────
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./patients.db")

    # ── API ─────────────────────────────────────────────────────
    API_V1_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # ── CORS ────────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # ── Subida de archivos ──────────────────────────────────────
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10 MB

    # ── Logging ─────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ── JWT / Autenticación ─────────────────────────────────────
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "goecosystem-super-secret-key-change-in-production-2025",
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # ── Usuario administrador inicial ───────────────────────────
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin123*")

    # ── Metadatos para Swagger ──────────────────────────────────
    APP_DESCRIPTION: str = (
        "Sistema de administración de pacientes para GoEcosystem Digital Health.\n\n"
        "### Características\n\n"
        "- CRUD completo de pacientes\n"
        "- Importación masiva desde Excel\n"
        "- Búsqueda por nombre o documento\n"
        "- Validación automática con Pydantic\n"
        "- Documentación interactiva Swagger\n\n"
        "### Autor\n\n"
        "**Alejandro Escandón**"
    )
    APP_CONTACT_NAME: str = "Alejandro Escandón"
    APP_CONTACT_URL: str = "https://github.com/alejandro-escandon"
    APP_LICENSE_NAME: str = "MIT"

    @property
    def is_production(self) -> bool:
        """Retorna True si el entorno es producción."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def base_dir(self) -> Path:
        """Retorna el directorio base del backend."""
        return Path(__file__).resolve().parent.parent

    @property
    def upload_path(self) -> Path:
        """Retorna la ruta completa de la carpeta de uploads."""
        return self.base_dir / self.UPLOAD_FOLDER

    @property
    def logs_path(self) -> Path:
        """Retorna la ruta completa de la carpeta de logs."""
        return self.base_dir / "logs"


settings = Settings()
