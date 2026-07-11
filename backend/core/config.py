"""Configuración de la aplicación mediante variables de entorno."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Clase de configuración centralizada de la aplicación."""

    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./patients.db")

    # Aplicación
    APP_NAME: str = os.getenv("APP_NAME", "GoEcosystem API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
