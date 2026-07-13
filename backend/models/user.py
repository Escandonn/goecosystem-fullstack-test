"""Modelo de la entidad Usuario para autenticación y RBAC."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from database.base import Base


class User(Base):
    """Representa un usuario del sistema con rol para control de acceso (RBAC)."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Datos personales
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True, index=True)

    # Credenciales
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    # Control de acceso
    rol = Column(String(20), nullable=False, default="user")  # admin / user
    activo = Column(Boolean, default=True, nullable=False)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', rol='{self.rol}')>"
