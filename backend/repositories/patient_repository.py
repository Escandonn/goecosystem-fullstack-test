"""Repositorio de la entidad Paciente."""

from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
        return self.db.query(Patient).filter(Patient.paciente_id == patient_id).first()

    def get_by_documento(self, documento: str) -> Optional[Patient]:
        """Busca un paciente por su número de documento."""
        return self.db.query(Patient).filter(Patient.documento == documento).first()

    def get_existing_documents(self, documentos: List[str]) -> set:
        """Retorna un set de números de documento que ya existen en la BD."""
        existing = (
            self.db.query(Patient.documento)
            .filter(Patient.documento.in_(documentos))
            .all()
        )
        return {doc[0] for doc in existing}

    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Busca pacientes por nombre completo o documento."""
        return (
            self.db.query(Patient)
            .filter(
                (Patient.nombre_completo.ilike(f"%{query}%"))
                | (Patient.documento.ilike(f"%{query}%"))
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

    def create_batch(self, patients_data: List[Dict[str, Any]]) -> tuple:
        """
        Crea múltiples pacientes en batch.
        
        Returns:
            tuple: (inserted_count, duplicate_count, error_count, ids_insertados, errors)
        """
        inserted = 0
        duplicates = 0
        errors = 0
        ids_insertados = []
        error_list = []
        
        # Extraer números de documento para verificar duplicados
        documentos = [p.get("documento") for p in patients_data if p.get("documento")]
        existing_docs = self.get_existing_documents(documentos) if documentos else set()
        
        for patient_data in patients_data:
            row_num = patient_data.pop("_row", None)
            
            # Verificar si el documento ya existe
            doc_val = patient_data.get("documento")
            if doc_val in existing_docs:
                duplicates += 1
                continue
            
            try:
                patient = Patient(**patient_data)
                self.db.add(patient)
                self.db.flush()  # Obtener el ID sin hacer commit
                ids_insertados.append(patient.paciente_id)
                inserted += 1
                existing_docs.add(doc_val)  # Evitar duplicados dentro del mismo batch
            except IntegrityError:
                self.db.rollback()
                duplicates += 1
                error_list.append({
                    "row": row_num,
                    "error": f"Documento duplicado: {doc_val}"
                })
            except Exception as e:
                errors += 1
                error_list.append({
                    "row": row_num,
                    "error": str(e)
                })
        
        if inserted > 0:
            self.db.commit()
        
        return inserted, duplicates, errors, ids_insertados, error_list

    def update(self, patient: Patient) -> Patient:
        """Actualiza un paciente existente."""
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient: Patient) -> None:
        """Elimina un paciente."""
        self.db.delete(patient)
        self.db.commit()
