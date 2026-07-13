"""Rutas de la API para la entidad Paciente."""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from schemas.import_result import ImportResult
from services.patient_service import PatientService

router = APIRouter(prefix="/pacientes")


@router.get("/", response_model=list[PatientResponse], tags=["Pacientes"],
         summary="Listar todos los pacientes",
         description="Obtiene una lista paginada de todos los pacientes registrados en el sistema.")
def list_pacientes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db),
):
    """Obtiene la lista de todos los pacientes."""
    service = PatientService(db)
    return service.get_all(skip=skip, limit=limit)


@router.get("/search", response_model=list[PatientResponse], tags=["Pacientes"],
         summary="Buscar pacientes",
         description="Busca pacientes por nombres, apellidos o número de documento (búsqueda parcial, case-insensitive).")
def search_pacientes(
    q: str = Query(..., min_length=1, description="Término de búsqueda (nombre, apellido o documento)"),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    db: Session = Depends(get_db),
):
    """Busca pacientes por nombre, apellido o número de documento."""
    service = PatientService(db)
    return service.search(q, skip=skip, limit=limit)


@router.get("/count", tags=["Pacientes"],
         summary="Contar pacientes",
         description="Retorna el número total de pacientes registrados en la base de datos.")
def count_pacientes(db: Session = Depends(get_db)):
    """Cuenta el total de pacientes registrados."""
    service = PatientService(db)
    return {"total": service.count()}


@router.get("/{patient_id}", response_model=PatientResponse, tags=["Pacientes"],
         summary="Obtener paciente por ID",
         description="Obtiene un paciente específico por su identificador único.",
         responses={404: {"description": "Paciente no encontrado"}})
def get_paciente(patient_id: int, db: Session = Depends(get_db)):
    """Obtiene un paciente por su ID."""
    service = PatientService(db)
    return service.get_by_id(patient_id)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED,
               tags=["Pacientes"],
               summary="Crear nuevo paciente",
               description="Crea un nuevo paciente en el sistema. El número de documento debe ser único.",
               responses={409: {"description": "Ya existe un paciente con ese número de documento"}})
def create_paciente(patient: PatientCreate, db: Session = Depends(get_db)):
    """Crea un nuevo paciente."""
    service = PatientService(db)
    return service.create(patient)


@router.put("/{patient_id}", response_model=PatientResponse, tags=["Pacientes"],
               summary="Actualizar paciente",
               description="Actualiza los datos de un paciente existente. Solo se modifican los campos enviados.",
               responses={404: {"description": "Paciente no encontrado"},
                          409: {"description": "Conflicto con número de documento"}})
def update_paciente(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    """Actualiza un paciente existente."""
    service = PatientService(db)
    return service.update(patient_id, patient)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pacientes"],
               summary="Eliminar paciente",
               description="Elimina permanentemente un paciente por su ID.",
               responses={404: {"description": "Paciente no encontrado"}})
def delete_paciente(patient_id: int, db: Session = Depends(get_db)):
    """Elimina un paciente por su ID."""
    service = PatientService(db)
    service.delete(patient_id)
    return None


@router.post("/importar", response_model=ImportResult, status_code=status.HTTP_200_OK,
                tags=["Importación"],
                summary="Importar pacientes desde Excel",
                description="Sube un archivo Excel (.xlsx) e importa pacientes masivamente.")
def importar_pacientes(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx) con los pacientes a importar"),
    db: Session = Depends(get_db),
):
    """
    Importa pacientes desde un archivo Excel.
    
    El archivo Excel debe contener las siguientes columnas:
    - **TipoDocumento**: Tipo de documento (CC, CE, TI, etc.)
    - **NumeroDocumento**: Número de documento (único)
    - **Nombres**: Nombres del paciente
    - **Apellidos**: Apellidos del paciente
    - **FechaNacimiento**: Fecha de nacimiento (YYYY-MM-DD)
    - **Sexo**: Sexo (M, F, Otro)
    
    Columnas opcionales:
    - **Telefono**: Número de teléfono
    - **Correo**: Correo electrónico
    - **Direccion**: Dirección de residencia
    - **Estado**: Estado del paciente (True/False, por defecto True)
    
    Retorna un resumen con:
    - Total de registros procesados
    - Pacientes insertados exitosamente
    - Documentos duplicados (ya existen)
    - Errores encontrados con detalles
    """
    service = PatientService(db)
    return service.import_from_excel(file)
