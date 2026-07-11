"""Servicio de lógica de negocio para la entidad Paciente."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.patient import Patient
from repositories.patient_repository import PatientRepository
from schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    """Contiene la lógica de negocio de pacientes."""

    def __init__(self, db: Session):
        self.repository = PatientRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Obtiene todos los pacientes."""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, patient_id: int) -> Patient:
        """Obtiene un paciente por ID o lanza 404."""
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Paciente con ID {patient_id} no encontrado",
            )
        return patient

    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Busca pacientes por nombre, apellido o documento."""
        return self.repository.search(query, skip=skip, limit=limit)

    def count(self) -> int:
        """Cuenta el total de pacientes."""
        return self.repository.count()

    def create(self, patient_data: PatientCreate) -> Patient:
        """Crea un paciente validando duplicados."""
        existing = self.repository.get_by_documento(patient_data.numero_documento)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un paciente con el documento '{patient_data.numero_documento}'",
            )
        patient = Patient(**patient_data.model_dump())
        return self.repository.create(patient)

    def update(self, patient_id: int, patient_data: PatientUpdate) -> Patient:
        """Actualiza un paciente existente."""
        patient = self.get_by_id(patient_id)

        # Si se actualiza el documento, verificar que no exista en otro paciente
        if patient_data.numero_documento and patient_data.numero_documento != patient.numero_documento:
            existing = self.repository.get_by_documento(patient_data.numero_documento)
            if existing and existing.id != patient_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un paciente con el documento '{patient_data.numero_documento}'",
                )

        update_data = patient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)

        return self.repository.update(patient)

    def delete(self, patient_id: int) -> None:
        """Elimina un paciente."""
        patient = self.get_by_id(patient_id)
        self.repository.delete(patient)
