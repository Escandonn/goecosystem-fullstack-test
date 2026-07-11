"""Endpoint de verificación de salud de la aplicación."""

from fastapi import APIRouter

from core.config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    """Verifica que la aplicación esté funcionando correctamente."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
