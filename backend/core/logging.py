"""Sistema de logging centralizado para GoEcosystem API."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from core.config import settings


# Formato de logs
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> logging.Logger:
    """
    Configura el sistema de logging global de la aplicación.

    - Handler de consola (stdout) con nivel INFO
    - Handler de archivo rotativo (logs/app.log) con nivel DEBUG
    - Formato unificado con timestamp, nivel, logger y mensaje

    Returns:
        logging.Logger: Logger raíz configurado para 'goecosystem'
    """
    # Asegurar que el directorio de logs exista
    logs_dir = settings.logs_path
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Logger raíz de la aplicación
    logger = logging.getLogger("goecosystem")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Evitar duplicar handlers si ya fue configurado
    if logger.handlers:
        return logger

    # Formatter compartido
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # ── Handler de consola ──────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ── Handler de archivo rotativo (5 MB por archivo, 3 backups) ──
    file_handler = RotatingFileHandler(
        filename=logs_dir / "app.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Reducir verbosidad de librerías de terceros
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger.info("Sistema de logging inicializado | nivel=%s | env=%s",
                settings.LOG_LEVEL, settings.ENVIRONMENT)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger hijo del logger raíz 'goecosystem'.

    Args:
        name: Nombre del módulo (ej. 'patient_service', 'patient_repository')

    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(f"goecosystem.{name}")
