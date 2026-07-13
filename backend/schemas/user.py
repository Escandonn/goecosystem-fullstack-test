"""Schemas de Pydantic para la entidad Usuario."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Campos base compartidos entre schemas de User."""

    nombre: str = Field(..., max_length=100, description="Nombres del usuario")
    apellido: str = Field(..., max_length=100, description="Apellidos del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico único")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    rol: str = Field("user", max_length=20, description="Rol: admin o user")

    @field_validator("rol")
    @classmethod
    def validate_rol(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in ("admin", "user"):
            raise ValueError("El rol debe ser 'admin' o 'user'")
        return v


class UserCreate(UserBase):
    """Schema para crear un nuevo usuario (incluye contraseña)."""

    password: str = Field(..., min_length=8, max_length=128, description="Contraseña (mínimo 8 caracteres)")


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario (todos los campos opcionales)."""

    nombre: Optional[str] = Field(None, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    correo: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    rol: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator("rol")
    @classmethod
    def validate_rol(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().lower()
        if v not in ("admin", "user"):
            raise ValueError("El rol debe ser 'admin' o 'user'")
        return v


class UserResponse(BaseModel):
    """Schema de respuesta para un usuario (sin contraseña)."""

    id: int
    nombre: str
    apellido: str
    correo: str
    username: str
    rol: str
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
