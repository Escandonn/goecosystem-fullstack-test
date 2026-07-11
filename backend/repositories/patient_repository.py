"""Repositorio de la entidad Paciente."""

from typing import Optional

from sqlalchemy.orm import Session

from models.patient import Patient


class PatientRepository:
    """Gestiona el acceso a datos de la entidad Patient."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Obtiene todos los pacientes con paginación."""
        return self.db.query(Patient).offset(skip).limit(limit).all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        """Busca un paciente por su ID."""
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def get_by_documento(self, numero_documento: str) -> Optional[Patient]:
        """Busca un paciente por su número de documento."""
        return self.db.query(Patient).filter(Patient.numero_documento == numero_documento).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Busca pacientes por nombres o apellidos."""
        return (
            self.db.query(Patient)
            .filter(
                (Patient.nombres.ilike(f"%{query}%"))
                | (Patient.apellidos.ilike(f"%{query}%"))
                | (Patient.numero_documento.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        """Cuenta el total de pacientes."""
        return self.db.query(Patient).count()

    def create(self, patient: Patient) -> Patient:
        """Crea un nuevo paciente."""
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def update(self, patient: Patient) -> Patient:
        """Actualiza un paciente existente."""
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient: Patient) -> None:
        """Elimina un paciente."""
        self.db.delete(patient)
        self.db.commit()
