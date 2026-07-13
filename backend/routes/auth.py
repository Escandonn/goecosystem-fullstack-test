"""Rutas de autenticación: login y perfil del usuario actual."""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from core.exceptions import BadRequestError
from database.session import get_db
from models.user import User
from schemas.auth import LoginRequest, Token
from schemas.user import UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    response_model=Token,
    tags=["Auth"],
    summary="Iniciar sesión",
    description="Autentica un usuario y retorna un token JWT para acceder a los endpoints protegidos.",
    responses={
        401: {"description": "Credenciales incorrectas"},
    },
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Inicia sesión con username y contraseña.

    Compatible con el flujo OAuth2 de Swagger UI (botón **Authorize**).
    """
    service = UserService(db)
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise BadRequestError("Usuario o contraseña incorrectos")
    return service.create_token(user)


@router.post(
    "/login/json",
    response_model=Token,
    tags=["Auth"],
    summary="Iniciar sesión (JSON)",
    description="Variante del login que acepta un body JSON en lugar de form-data.",
    responses={
        401: {"description": "Credenciales incorrectas"},
    },
)
def login_json(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    """Inicia sesión enviando las credenciales como JSON."""
    service = UserService(db)
    user = service.authenticate(credentials.username, credentials.password)
    if not user:
        raise BadRequestError("Usuario o contraseña incorrectos")
    return service.create_token(user)


@router.get(
    "/me",
    response_model=UserResponse,
    tags=["Auth"],
    summary="Obtener perfil del usuario actual",
    description="Retorna la información del usuario autenticado a partir del token JWT.",
    responses={
        401: {"description": "No autorizado"},
    },
)
def get_me(current_user: User = Depends(get_current_user)):
    """Retorna el perfil del usuario autenticado."""
    return current_user
