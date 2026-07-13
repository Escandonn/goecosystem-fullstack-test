"""Rutas de la API para gestión de usuarios (solo admin)."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from auth.dependencies import require_admin
from database.session import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/users")


@router.get(
    "/",
    response_model=list[UserResponse],
    tags=["Usuarios"],
    summary="Listar todos los usuarios",
    description="Obtiene una lista paginada de todos los usuarios registrados. **Requiere rol admin.**",
)
def list_usuarios(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Lista todos los usuarios (solo admin)."""
    service = UserService(db)
    return service.get_all(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    tags=["Usuarios"],
    summary="Obtener usuario por ID",
    description="Obtiene un usuario específico por su ID. **Requiere rol admin.**",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Obtiene un usuario por su ID (solo admin)."""
    service = UserService(db)
    return service.get_by_id(user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
    summary="Crear nuevo usuario",
    description="Crea un nuevo usuario en el sistema. **Requiere rol admin.**",
    responses={409: {"description": "Username o correo ya existe"}},
)
def create_usuario(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Crea un nuevo usuario (solo admin)."""
    service = UserService(db)
    return service.create(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    tags=["Usuarios"],
    summary="Actualizar usuario",
    description="Actualiza los datos de un usuario existente. **Requiere rol admin.**",
    responses={
        404: {"description": "Usuario no encontrado"},
        409: {"description": "Username o correo ya existe"},
    },
)
def update_usuario(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Actualiza un usuario existente (solo admin)."""
    service = UserService(db)
    return service.update(user_id, user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Usuarios"],
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario por su ID. **Requiere rol admin.**",
    responses={404: {"description": "Usuario no encontrado"}},
)
def delete_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Elimina un usuario por su ID (solo admin)."""
    service = UserService(db)
    service.delete(user_id)
    return None
