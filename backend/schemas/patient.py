"""Schemas de Pydantic para la entidad Paciente."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class PatientBase(BaseModel):
    """Campos base compartidos entre todos los schemas de Patient."""

    tipo_documento: str = Field(..., max_length=20, description="Tipo de documento (CC, TI, CE, etc.)")
    numero_documento: str = Field(..., max_length=50, description="Número de documento único")
    nombres: str = Field(..., max_length=100, description="Nombres del paciente")
    apellidos: str = Field(..., max_length=100, description="Apellidos del paciente")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")
    sexo: str = Field(..., max_length=10, description="Sexo: M, F u Otro")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    correo: Optional[EmailStr] = Field(None, description="Correo electrónico válido")
    direccion: Optional[str] = Field(None, max_length=255, description="Dirección de residencia")
    estado: str = Field("Activo", max_length=20, description="Estado: Activo o Inactivo")

    @field_validator("sexo")
    @classmethod
    def validate_sexo(cls, v: str) -> str:
        v = v.strip().capitalize()
        if v not in ("M", "F", "Otro"):
            raise ValueError("El sexo debe ser 'M', 'F' u 'Otro'")
        return v

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v) -> str:
        # Handle boolean from database (1, 0, True, False, '1', '0')
        if isinstance(v, bool):
            return "Activo" if v else "Inactivo"
        if isinstance(v, (int, float)):
            return "Activo" if v else "Inactivo"
        # Handle string representations of boolean
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped in ("1", "True", "true", "T", "t"):
                return "Activo"
            if v_stripped in ("0", "False", "false", "F", "f"):
                return "Inactivo"
            # Normalize string
            v_stripped = v_stripped.capitalize()
            if v_stripped in ("Activo", "Inactivo"):
                return v_stripped
        raise ValueError("El estado debe ser 'Activo' o 'Inactivo'")


class PatientCreate(PatientBase):
    """Schema para crear un nuevo paciente."""

    pass


class PatientUpdate(BaseModel):
    """Schema para actualizar un paciente (todos los campos opcionales)."""

    tipo_documento: Optional[str] = Field(None, max_length=20)
    numero_documento: Optional[str] = Field(None, max_length=50)
    nombres: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = Field(None, max_length=10)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=255)
    estado: Optional[str] = Field(None, max_length=20)

    @field_validator("sexo")
    @classmethod
    def validate_sexo(cls, v):
        if v is None:
            return v
        v = v.strip().capitalize()
        if v not in ("M", "F", "Otro"):
            raise ValueError("El sexo debe ser 'M', 'F' u 'Otro'")
        return v

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v):
        if v is None:
            return v
        # Handle boolean from database (1, 0, True, False, '1', '0')
        if isinstance(v, bool):
            return "Activo" if v else "Inactivo"
        if isinstance(v, (int, float)):
            return "Activo" if v else "Inactivo"
        # Handle string representations of boolean
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped in ("1", "True", "true", "T", "t"):
                return "Activo"
            if v_stripped in ("0", "False", "false", "F", "f"):
                return "Inactivo"
            # Normalize string
            v_stripped = v_stripped.capitalize()
            if v_stripped in ("Activo", "Inactivo"):
                return v_stripped
        raise ValueError("El estado debe ser 'Activo' o 'Inactivo'")


class PatientResponse(PatientBase):
    """Schema de respuesta que incluye campos generados por la base de datos."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
