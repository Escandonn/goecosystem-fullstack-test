"""Schemas de Pydantic para autenticación (login y tokens JWT)."""

from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Credenciales para iniciar sesión."""

    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña en texto plano")


class Token(BaseModel):
    """Respuesta del endpoint de login con el token JWT."""

    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field("bearer", description="Tipo de token")
    username: str = Field(..., description="Nombre de usuario autenticado")
    rol: str = Field(..., description="Rol del usuario")


class TokenData(BaseModel):
    """Datos extraídos del token JWT."""

    username: Optional[str] = None
    rol: Optional[str] = None
