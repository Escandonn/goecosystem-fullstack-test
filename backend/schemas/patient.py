"""Schemas de Pydantic para la entidad Paciente."""

from datetime import date, datetime
from typing import Optional, Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class PatientBase(BaseModel):
    """Campos base compartidos entre todos los schemas de Patient."""

    tipo_documento: str = Field(..., max_length=3, description="Tipo de documento (CC, TI, CE, PA)")
    documento: str = Field(..., max_length=20, description="Número de documento único")
    nombre_completo: str = Field(..., max_length=150, description="Nombre completo del paciente")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")
    genero: str = Field(..., max_length=30, description="Género del paciente (Masculino, Femenino, No binario, Prefiere no responder)")
    telefono: str = Field(..., max_length=20, description="Teléfono de contacto")
    correo: Optional[str] = Field(None, description="Correo electrónico con dominio example.test")
    eps_codigo: str = Field(..., max_length=10, description="Código de la EPS")
    eps_nombre: str = Field(..., max_length=100, description="Nombre de la EPS")
    ciudad: Optional[str] = Field(None, max_length=80, description="Ciudad de residencia")
    prioridad: str = Field(..., max_length=10, description="Prioridad: Alta, Media o Baja")
    estado: str = Field("Pendiente", max_length=20, description="Estado: Pendiente, En atención o Atendido")

    @field_validator("tipo_documento")
    @classmethod
    def validate_tipo_documento(cls, v: str) -> str:
        v = v.strip().upper()
        if v not in ("CC", "TI", "CE", "PA"):
            raise ValueError("El tipo de documento debe ser CC, TI, CE o PA")
        return v

    @field_validator("fecha_nacimiento", mode="before")
    @classmethod
    def validate_fecha_nacimiento(cls, v: Any) -> date:
        if isinstance(v, str):
            try:
                v = date.fromisoformat(v)
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en formato YYYY-MM-DD")
        elif isinstance(v, datetime):
            v = v.date()
        if not isinstance(v, date):
            raise ValueError("La fecha de nacimiento no es una fecha válida")
        if v > date.today():
            raise ValueError("La fecha de nacimiento no puede ser posterior a la fecha actual")
        return v

    @field_validator("genero")
    @classmethod
    def validate_genero(cls, v: str) -> str:
        v = v.strip().capitalize()
        if v not in ("Masculino", "Femenino", "No binario", "Prefiere no responder"):
            raise ValueError("El género debe ser 'Masculino', 'Femenino', 'No binario' o 'Prefiere no responder'")
        return v

    @field_validator("prioridad")
    @classmethod
    def validate_prioridad(cls, v: str) -> str:
        v = v.strip().capitalize()
        if v not in ("Alta", "Media", "Baja"):
            raise ValueError("La prioridad debe ser 'Alta', 'Media' o 'Baja'")
        return v

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v: str) -> str:
        if isinstance(v, str):
            v_norm = v.strip().lower()
            if v_norm in ("en atención", "en atencion"):
                return "En atención"
            if v_norm == "pendiente":
                return "Pendiente"
            if v_norm == "atendido":
                return "Atendido"
        raise ValueError("El estado debe ser 'Pendiente', 'En atención' o 'Atendido'")

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if not v.endswith("@example.test"):
                raise ValueError("El correo debe pertenecer al dominio @example.test")
        return v


class PatientCreate(PatientBase):
    """Schema para crear un nuevo paciente."""

    pass


class PatientUpdate(BaseModel):
    """Schema para actualizar un paciente (todos los campos opcionales)."""

    tipo_documento: Optional[str] = Field(None, max_length=3)
    documento: Optional[str] = Field(None, max_length=20)
    nombre_completo: Optional[str] = Field(None, max_length=150)
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = Field(None, max_length=30)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = None
    eps_codigo: Optional[str] = Field(None, max_length=10)
    eps_nombre: Optional[str] = Field(None, max_length=100)
    ciudad: Optional[str] = Field(None, max_length=80)
    prioridad: Optional[str] = Field(None, max_length=10)
    estado: Optional[str] = Field(None, max_length=20)

    @field_validator("tipo_documento")
    @classmethod
    def validate_tipo_documento(cls, v):
        if v is None:
            return v
        v = v.strip().upper()
        if v not in ("CC", "TI", "CE", "PA"):
            raise ValueError("El tipo de documento debe ser CC, TI, CE o PA")
        return v

    @field_validator("fecha_nacimiento", mode="before")
    @classmethod
    def validate_fecha_nacimiento(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                v = date.fromisoformat(v)
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en formato YYYY-MM-DD")
        elif isinstance(v, datetime):
            v = v.date()
        if not isinstance(v, date):
            raise ValueError("La fecha de nacimiento no es una fecha válida")
        if v > date.today():
            raise ValueError("La fecha de nacimiento no puede ser posterior a la fecha actual")
        return v

    @field_validator("genero")
    @classmethod
    def validate_genero(cls, v):
        if v is None:
            return v
        v = v.strip().capitalize()
        if v not in ("Masculino", "Femenino", "No binario", "Prefiere no responder"):
            raise ValueError("El género debe ser 'Masculino', 'Femenino', 'No binario' o 'Prefiere no responder'")
        return v

    @field_validator("prioridad")
    @classmethod
    def validate_prioridad(cls, v):
        if v is None:
            return v
        v = v.strip().capitalize()
        if v not in ("Alta", "Media", "Baja"):
            raise ValueError("La prioridad debe ser 'Alta', 'Media' o 'Baja'")
        return v

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            v_norm = v.strip().lower()
            if v_norm in ("en atención", "en atencion"):
                return "En atención"
            if v_norm == "pendiente":
                return "Pendiente"
            if v_norm == "atendido":
                return "Atendido"
        raise ValueError("El estado debe ser 'Pendiente', 'En atención' o 'Atendido'")

    @field_validator("correo")
    @classmethod
    def validate_correo(cls, v):
        if v is None:
            return v
        v = v.strip().lower()
        if not v.endswith("@example.test"):
            raise ValueError("El correo debe pertenecer al dominio @example.test")
        return v


class PatientResponse(PatientBase):
    """Schema de respuesta que incluye campos generados por la base de datos."""

    paciente_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}
