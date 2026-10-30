from argon2.exceptions import HashingError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.users.exceptions import (
    UserAlreadyExistsError,
    UserPasswordHashError,
)
from app.features.users.schemas import UserCreate, UserRead, UserUpdate
from app.models.db import Project, User
from app.shared.exceptions import ProjectNotFoundError
from app.utils.model_to_read import user_to_read

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
        raise UserPasswordHashError("Unable to securely hash the password.") from exc

    user = User(
        username=payload.username,
        password_hash=hashed_password,
    )

    db.add(user)
    db.flush()
    db.refresh(user)

    return user_to_read(user)


def update_user(
    db: Session,
    user: User,
    payload: UserUpdate,
) -> UserRead:
    project = db.execute(
        select(Project).where(
            Project.public_id == payload.active_project_public_id,
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(
            f"Project with public_id {payload.active_project_public_id} not found"
        )

    user.active_project = project
    db.flush()

    return user_to_read(user)
