"""Repositorio de la entidad Usuario."""

from typing import Optional

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    """Gestiona el acceso a datos de la entidad User."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Obtiene todos los usuarios con paginación."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_correo(self, correo: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        return self.db.query(User).filter(User.correo == correo).first()

    def count(self) -> int:
        """Cuenta el total de usuarios."""
        return self.db.query(User).count()

    def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Elimina un usuario."""
        self.db.delete(user)
        self.db.commit()
