"""Esquema OAuth2 para integración con Swagger UI."""

from fastapi.security import OAuth2PasswordBearer

from core.config import settings

# Token URL relativa al prefijo de la API: /api/v1/auth/login
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    scheme_name="JWT",
    description="Introduce tu usuario y contraseña para obtener un token JWT.",
)
