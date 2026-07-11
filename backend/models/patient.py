"""Modelo de la entidad Paciente."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from database.base import Base


class Patient(Base):
    """Representa un paciente en el sistema de gestión clínica."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    # Documento de identidad
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(50), nullable=False, unique=True, index=True)

    # Datos personales
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(String(10), nullable=False)  # ISO format: YYYY-MM-DD
    sexo = Column(String(10), nullable=False)  # M / F / Otro

    # Contacto
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)

    # Estado del paciente
    estado = Column(String(20), nullable=False, default="Activo")  # Activo / Inactivo

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, nombres='{self.nombres}', apellidos='{self.apellidos}')>"
