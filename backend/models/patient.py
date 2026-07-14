"""Modelo de la entidad Paciente."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime

from database.base import Base


class Patient(Base):
    """Representa un paciente en el sistema de gestión clínica."""

    __tablename__ = "patients"

    paciente_id = Column(Integer, primary_key=True, index=True)

    # Documento de identidad
    tipo_documento = Column(String(3), nullable=False)
    documento = Column(String(20), nullable=False, unique=True, index=True)

    # Datos personales
    nombre_completo = Column(String(150), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String(30), nullable=False)

    # Contacto
    telefono = Column(String(20), nullable=False)
    correo = Column(String(150), nullable=True)
    eps_codigo = Column(String(10), nullable=False)
    eps_nombre = Column(String(100), nullable=False)
    ciudad = Column(String(80), nullable=True)

    # Gestión de lista
    prioridad = Column(String(10), nullable=False)
    estado = Column(String(20), nullable=False, default="Pendiente")

    # Auditoría
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Patient(paciente_id={self.paciente_id}, nombre_completo='{self.nombre_completo}', documento='{self.documento}')>"
