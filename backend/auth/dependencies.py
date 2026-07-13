"""Dependencias de FastAPI para autenticación y control de acceso por roles (RBAC)."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.jwt import oauth2_scheme
from core.security import decode_access_token
from database.session import get_db
from models.user import User


# ── Excepciones reutilizables ───────────────────────────────────
_credential_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)

_forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tienes permisos para realizar esta acción",
)


# ═══════════════════════════════════════════════════════════════
#  Dependencia: obtener usuario actual desde el token
# ═══════════════════════════════════════════════════════════════

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Extrae y valida el token JWT del header Authorization.

    Retorna el objeto User correspondiente o lanza 401.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise _credential_error

    username: Optional[str] = payload.get("sub")
    if username is None:
        raise _credential_error

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise _credential_error

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacta al administrador.",
        )

    return user


# ═══════════════════════════════════════════════════════════════
#  Dependencia: requerir un rol específico (RBAC)
# ═══════════════════════════════════════════════════════════════

def require_role(allowed_roles: list[str]):
    """
    Fábrica de dependencias que verifica si el usuario actual
    tiene uno de los roles permitidos.

    Uso:
        current_user: User = Depends(require_role(["admin"]))
    """
    def _check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol not in allowed_roles:
            raise _forbidden_error
        return current_user
    return _check_role


# ── Atajos para roles comunes ───────────────────────────────────

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependencia que requiere rol 'admin'."""
    if current_user.rol != "admin":
        raise _forbidden_error
    return current_user
