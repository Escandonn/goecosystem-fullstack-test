"""Endpoint de verificación de salud de la aplicación."""

from fastapi import APIRouter

from core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"],
            summary="Verificación de salud",
            description="Verifica que la aplicación esté funcionando correctamente. "
                        "Retorna el estado, nombre y versión de la API.")
def health_check():
    """Verifica que la aplicación esté funcionando correctamente."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
