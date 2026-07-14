"""Excepciones personalizadas y handlers globales para GoEcosystem API."""

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.config import settings


# ═══════════════════════════════════════════════════════════════
#  Excepciones personalizadas
# ═══════════════════════════════════════════════════════════════

class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(
        self,
        message: str = "Error interno del servidor",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class BadRequestError(AppException):
    """Error 400 - Solicitud incorrecta."""

    def __init__(self, message: str = "Solicitud incorrecta", details: Optional[dict] = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class NotFoundError(AppException):
    """Error 404 - Recurso no encontrado."""

    def __init__(self, message: str = "Recurso no encontrado", details: Optional[dict] = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class ConflictError(AppException):
    """Error 409 - Conflicto (ej. duplicado)."""

    def __init__(self, message: str = "Conflicto con el recurso existente", details: Optional[dict] = None):
        super().__init__(message, status.HTTP_409_CONFLICT, details)


class ValidationError(AppException):
    """Error 422 - Error de validación de datos."""

    def __init__(self, message: str = "Error de validación", details: Optional[dict] = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


# ═══════════════════════════════════════════════════════════════
#  Formato de respuesta estandarizado
# ═══════════════════════════════════════════════════════════════

def _error_response(
    message: str,
    status_code: int,
    details: Optional[dict] = None,
) -> JSONResponse:
    """
    Construye una respuesta JSON de error estandarizada.

    Formato:
        {
            "success": false,
            "message": "Paciente no encontrado",
            "status_code": 404,
            "timestamp": "2025-01-15T10:30:00Z",
            "details": { ... }
        }
    """
    body: dict[str, Any] = {
        "success": False,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if details:
        body["details"] = details
    return JSONResponse(status_code=status_code, content=body)


# ═══════════════════════════════════════════════════════════════
#  Handlers globales
# ═══════════════════════════════════════════════════════════════

def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos los handlers de excepciones en la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI
    """

    # ── Excepciones personalizadas de la app ───────────────────
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return _error_response(exc.message, exc.status_code, exc.details)

    # ── HTTPException de FastAPI/Starlette ──────────────────────
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        # Mapear códigos comunes a mensajes descriptivos
        default_messages = {
            400: "Solicitud incorrecta",
            401: "No autorizado",
            403: "Acceso prohibido",
            404: "Recurso no encontrado",
            405: "Método no permitido",
            422: "Entidad no procesable",
            429: "Demasiadas solicitudes",
            500: "Error interno del servidor",
        }
        message = exc.detail if isinstance(exc.detail, str) else default_messages.get(exc.status_code, "Error")
        return _error_response(message, exc.status_code)

    # ── Error de validación de Pydantic (422) ───────────────────
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = []
        for error in exc.errors():
            sanitized_error = error.copy()
            if "ctx" in sanitized_error and isinstance(sanitized_error["ctx"], dict):
                ctx = sanitized_error["ctx"].copy()
                if "error" in ctx and isinstance(ctx["error"], Exception):
                    ctx["error"] = str(ctx["error"])
                sanitized_error["ctx"] = ctx
            errors.append(sanitized_error)
        return _error_response(
            "Error de validación de datos",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors},
        )

    # ── Excepción genérica no controlada (500) ──────────────────
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return _error_response(
            "Error interno del servidor",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"error": str(exc)} if settings.ENVIRONMENT != "production" else None,
        )
