"""Rutas de la API para la entidad Paciente."""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user, require_admin
from database.session import get_db
from models.user import User
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    """Busca pacientes por nombre, apellido o número de documento."""
    service = PatientService(db)
    return service.search(q, skip=skip, limit=limit)


@router.get("/count", tags=["Pacientes"],
         summary="Contar pacientes",
         description="Retorna el número total de pacientes registrados en la base de datos.")
def count_pacientes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cuenta el total de pacientes registrados."""
    service = PatientService(db)
    return {"total": service.count()}


@router.get("/{paciente_id}", response_model=PatientResponse, tags=["Pacientes"],
         summary="Obtener paciente por ID",
         description="Obtiene un paciente específico por su identificador único.",
         responses={404: {"description": "Paciente no encontrado"}})
def get_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtiene un paciente por su ID."""
    service = PatientService(db)
    return service.get_by_id(paciente_id)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED,
               tags=["Pacientes"],
               summary="Crear nuevo paciente",
               description="Crea un nuevo paciente en el sistema. El documento debe ser único.",
               responses={409: {"description": "Ya existe un paciente con ese documento"}})
def create_paciente(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crea un nuevo paciente."""
    service = PatientService(db)
    return service.create(patient)


@router.put("/{paciente_id}", response_model=PatientResponse, tags=["Pacientes"],
               summary="Actualizar paciente",
               description="Actualiza los datos de un paciente existente. Solo se modifican los campos enviados.",
               responses={404: {"description": "Paciente no encontrado"},
                          409: {"description": "Conflicto con documento"}})
def update_paciente(
    paciente_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualiza un paciente existente."""
    service = PatientService(db)
    return service.update(paciente_id, patient)


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pacientes"],
               summary="Eliminar paciente",
               description="Elimina permanentemente un paciente por su ID. **Requiere rol admin.**",
               responses={404: {"description": "Paciente no encontrado"},
                          403: {"description": "Acceso prohibido"}})
def delete_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Elimina un paciente por su ID (solo admin)."""
    service = PatientService(db)
    service.delete(paciente_id)
    return None


@router.post("/importar", response_model=ImportResult, status_code=status.HTTP_200_OK,
                tags=["Importación"],
                summary="Importar pacientes desde Excel",
                description="Sube un archivo Excel (.xlsx) e importa pacientes masivamente. **Requiere rol admin.**")
def importar_pacientes(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx) con los pacientes a importar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Importa pacientes desde un archivo Excel.
    
    El archivo Excel debe contener las siguientes columnas (en minúsculas):
    - **tipo_documento**: Tipo de documento (CC, CE, TI, PA)
    - **documento**: Número de documento (único, no se permiten duplicados)
    - **nombre_completo**: Nombre completo del paciente
    - **fecha_nacimiento**: Fecha de nacimiento (YYYY-MM-DD)
    - **genero**: Género (Masculino, Femenino, Otro)
    - **telefono**: Teléfono de contacto
    - **eps_codigo**: Código de la EPS
    - **eps_nombre**: Nombre de la EPS
    - **prioridad**: Prioridad (Alta, Media, Baja)
    - **estado**: Estado (Pendiente, En atención, Atendido)
    
    Columnas opcionales:
    - **correo**: Correo electrónico (debe terminar en @example.test)
    - **ciudad**: Ciudad de residencia
    
    Columnas ignoradas (generadas por la BD):
    - **paciente_id**, **fecha_creacion**, **fecha_actualizacion**
    
    No se permiten documentos duplicados: si un documento ya existe en la BD
    o está repetido dentro del mismo archivo, el registro se omite.
    
    Retorna un resumen con:
    - Total de registros procesados
    - Pacientes insertados exitosamente
    - Documentos duplicados (ya existen)
    - Errores encontrados con detalles
    """
    service = PatientService(db)
    return service.import_from_excel(file)
