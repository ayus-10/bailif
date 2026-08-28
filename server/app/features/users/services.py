from uuid import UUID

from argon2.exceptions import HashingError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.users.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserPasswordHashError,
)
from app.features.users.schemas import UserCreate
from app.models.db.user import User

password_hash = PasswordHash.recommended()


def create_user(
    db: Session,
    payload: UserCreate,
) -> User:
    existing_user = db.scalar(select(User).where(User.username == payload.username))

    if existing_user:
        raise UserAlreadyExistsError(
            f"Username '{payload.username}' is already in use."
        )

    try:
        hashed_password = password_hash.hash(payload.password)
    except HashingError as exc:
        raise UserPasswordHashError() from exc

    user = User(
        username=payload.username,
        password_hash=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: UUID,
) -> User:
    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise UserNotFoundError(f"User '{user_id}' not found.")

    return user


def login_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = db.scalar(select(User).where(User.username == username))

    if user is None:
        raise UserNotFoundError()

    if not password_hash.verify(password, user.password_hash):
        raise InvalidCredentialsError()

    return user
