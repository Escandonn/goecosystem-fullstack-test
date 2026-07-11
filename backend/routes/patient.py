"""Rutas de la API para la entidad Paciente."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from services.patient_service import PatientService

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=list[PatientResponse])
def list_pacientes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    db: Session = Depends(get_db),
):
    """Obtiene la lista de todos los pacientes."""
    service = PatientService(db)
    return service.get_all(skip=skip, limit=limit)


@router.get("/search", response_model=list[PatientResponse])
def search_pacientes(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Busca pacientes por nombre, apellido o número de documento."""
    service = PatientService(db)
    return service.search(q, skip=skip, limit=limit)


@router.get("/count")
def count_pacientes(db: Session = Depends(get_db)):
    """Cuenta el total de pacientes registrados."""
    service = PatientService(db)
    return {"total": service.count()}


@router.get("/{patient_id}", response_model=PatientResponse)
def get_paciente(patient_id: int, db: Session = Depends(get_db)):
    """Obtiene un paciente por su ID."""
    service = PatientService(db)
    return service.get_by_id(patient_id)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_paciente(patient: PatientCreate, db: Session = Depends(get_db)):
    """Crea un nuevo paciente."""
    service = PatientService(db)
    return service.create(patient)


@router.put("/{patient_id}", response_model=PatientResponse)
def update_paciente(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    """Actualiza un paciente existente."""
    service = PatientService(db)
    return service.update(patient_id, patient)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paciente(patient_id: int, db: Session = Depends(get_db)):
    """Elimina un paciente por su ID."""
    service = PatientService(db)
    service.delete(patient_id)
    return None
