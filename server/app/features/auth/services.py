from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.auth.exceptions import InvalidCredentialsError
from app.features.auth.schemas import UserRead
from app.models.db.user import User

password_hash = PasswordHash.recommended()


def login_user(
    db: Session,
    username: str,
    password: str,
) -> UserRead:
    user = db.scalar(select(User).where(User.username == username))

    if user is None:
        raise InvalidCredentialsError()

    if not password_hash.verify(password, user.password_hash):
        raise InvalidCredentialsError()

    return UserRead.model_validate(user)
