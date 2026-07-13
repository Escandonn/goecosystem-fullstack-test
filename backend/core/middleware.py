"""Middleware personalizado para GoEcosystem API."""

import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.logging import get_logger

logger = get_logger("middleware")


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que mide el tiempo de cada request y lo registra en logs.

    Agrega headers:
        X-Process-Time: tiempo en segundos (float)
        X-Request-ID: identificador único por request
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generar ID único para el request
        request_id = str(uuid.uuid4())[:8]

        # Timestamp de inicio
        start_time = time.perf_counter()

        # Log de entrada
        logger.info(
            "→ %s %s | request_id=%s",
            request.method,
            request.url.path,
            request_id,
        )

        # Ejecutar el request
        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            logger.error(
                "✗ %s %s | request_id=%s | error=%s | %.4fs",
                request.method,
                request.url.path,
                request_id,
                str(exc),
                elapsed,
            )
            raise

        # Calcular tiempo transcurrido
        elapsed = time.perf_counter() - start_time
        elapsed_ms = elapsed * 1000

        # Agregar headers de respuesta
        response.headers["X-Process-Time"] = f"{elapsed:.6f}"
        response.headers["X-Request-ID"] = request_id

        # Log de salida
        log_method = logger.info if response.status_code < 400 else logger.warning
        log_method(
            "← %s %s | request_id=%s | status=%d | %.2fms",
            request.method,
            request.url.path,
            request_id,
            response.status_code,
            elapsed_ms,
        )

        return response
