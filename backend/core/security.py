"""Utilidades de seguridad: hashing de contraseñas y gestión de tokens JWT."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings


# ── Contexto de hashing con bcrypt ──────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ═══════════════════════════════════════════════════════════════
#  Hashing de contraseñas
# ═══════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincida con su hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ═══════════════════════════════════════════════════════════════
#  Tokens JWT
# ═══════════════════════════════════════════════════════════════

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Crea un token JWT firmado.

    Args:
        data: Diccionario con los claims (debe incluir 'sub' = username).
        expires_delta: Tiempo de expiración personalizado.

    Returns:
        Token JWT codificado como string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT.

    Args:
        token: Token JWT en string.

    Returns:
        Diccionario con los claims del token, o None si es inválido/expirado.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
