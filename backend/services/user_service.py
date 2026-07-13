"""Servicio de lógica de negocio para la entidad Usuario."""

from typing import Optional

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError, ConflictError, BadRequestError
from core.logging import get_logger
from core.security import hash_password, verify_password, create_access_token
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate


logger = get_logger("user_service")


class UserService:
    """Contiene la lógica de negocio de usuarios y autenticación."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    # ═══════════════════════════════════════════════════════════
    #  Autenticación
    # ═══════════════════════════════════════════════════════════

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Valida las credenciales del usuario.

        Retorna el objeto User si las credenciales son correctas,
        o None si el usuario no existe o la contraseña no coincide.
        """
        user = self.repository.get_by_username(username)
        if not user:
            logger.warning("Intento de login con usuario inexistente | username=%s", username)
            return None
        if not user.activo:
            logger.warning("Intento de login con usuario inactivo | username=%s", username)
            return None
        if not verify_password(password, user.password_hash):
            logger.warning("Contraseña incorrecta | username=%s", username)
            return None
        logger.info("Usuario autenticado | username=%s", username)
        return user

    def create_token(self, user: User) -> dict:
        """Genera el token JWT y construye la respuesta del login."""
        token = create_access_token(
            data={"sub": user.username, "rol": user.rol}
        )
        logger.info("Token JWT generado | username=%s rol=%s", user.username, user.rol)
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "rol": user.rol,
        }

    # ═══════════════════════════════════════════════════════════
    #  CRUD de usuarios
    # ═══════════════════════════════════════════════════════════

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Obtiene todos los usuarios."""
        users = self.repository.get_all(skip=skip, limit=limit)
        logger.debug("get_all | skip=%d limit=%d | %d usuarios", skip, limit, len(users))
        return users

    def get_by_id(self, user_id: int) -> User:
        """Obtiene un usuario por ID o lanza 404."""
        user = self.repository.get_by_id(user_id)
        if not user:
            logger.warning("Usuario no encontrado | id=%d", user_id)
            raise NotFoundError(f"Usuario con ID {user_id} no encontrado")
        return user

    def create(self, user_data: UserCreate) -> User:
        """Crea un nuevo usuario validando duplicados de username y correo."""
        # Verificar username duplicado
        if self.repository.get_by_username(user_data.username):
            logger.warning("Username duplicado | username=%s", user_data.username)
            raise ConflictError(f"Ya existe un usuario con el username '{user_data.username}'")

        # Verificar correo duplicado
        if self.repository.get_by_correo(user_data.correo):
            logger.warning("Correo duplicado | correo=%s", user_data.correo)
            raise ConflictError(f"Ya existe un usuario con el correo '{user_data.correo}'")

        user = User(
            nombre=user_data.nombre,
            apellido=user_data.apellido,
            correo=user_data.correo,
            username=user_data.username,
            password_hash=hash_password(user_data.password),
            rol=user_data.rol,
            activo=True,
        )
        result = self.repository.create(user)
        logger.info("Usuario creado | id=%d username=%s rol=%s", result.id, result.username, result.rol)
        return result

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Actualiza un usuario existente."""
        user = self.get_by_id(user_id)

        # Validar username duplicado si se está cambiando
        if user_data.username and user_data.username != user.username:
            existing = self.repository.get_by_username(user_data.username)
            if existing and existing.id != user_id:
                raise ConflictError(f"Ya existe un usuario con el username '{user_data.username}'")
            user.username = user_data.username

        # Validar correo duplicado si se está cambiando
        if user_data.correo and user_data.correo != user.correo:
            existing = self.repository.get_by_correo(user_data.correo)
            if existing and existing.id != user_id:
                raise ConflictError(f"Ya existe un usuario con el correo '{user_data.correo}'")
            user.correo = user_data.correo

        # Campos simples
        if user_data.nombre is not None:
            user.nombre = user_data.nombre
        if user_data.apellido is not None:
            user.apellido = user_data.apellido
        if user_data.rol is not None:
            user.rol = user_data.rol
        if user_data.activo is not None:
            user.activo = user_data.activo

        # Contraseña (se hashea si se proporciona)
        if user_data.password:
            user.password_hash = hash_password(user_data.password)

        result = self.repository.update(user)
        logger.info("Usuario actualizado | id=%d", result.id)
        return result

    def delete(self, user_id: int) -> None:
        """Elimina un usuario por su ID."""
        user = self.get_by_id(user_id)
        self.repository.delete(user)
        logger.info("Usuario eliminado | id=%d", user_id)

    # ═══════════════════════════════════════════════════════════
    #  Inicialización: usuario administrador
    # ═══════════════════════════════════════════════════════════

    def ensure_admin_exists(self, username: str, password: str) -> None:
        """
        Crea el usuario administrador inicial si no existe.
        Se ejecuta al arrancar la aplicación.
        """
        existing = self.repository.get_by_username(username)
        if existing:
            logger.debug("Usuario admin ya existe | username=%s", username)
            return

        admin = User(
            nombre="Administrador",
            apellido="Sistema",
            correo="admin@goecosystem.com",
            username=username,
            password_hash=hash_password(password),
            rol="admin",
            activo=True,
        )
        self.repository.create(admin)
        logger.info("Usuario administrador inicial creado | username=%s", username)
