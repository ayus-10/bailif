from argon2.exceptions import HashingError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.users.exceptions import (
    UserAlreadyExistsError,
    UserPasswordHashError,
)
from app.features.users.schemas import UserCreate, UserRead
from app.models.db.user import User

password_hash = PasswordHash.recommended()


def create_user(
    db: Session,
    payload: UserCreate,
) -> UserRead:
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

    return UserRead.model_validate(user)
