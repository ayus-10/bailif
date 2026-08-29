from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.core.tokens as tokens
from app.features.auth.exceptions import InvalidCredentialsError
from app.models.db.user import User

password_hash = PasswordHash.recommended()


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = db.scalar(select(User).where(User.username == username))

    if user is None:
        raise InvalidCredentialsError()

    if not password_hash.verify(password, user.password_hash):
        raise InvalidCredentialsError()

    return user


def generate_access_token(user: User) -> str:
    return tokens.create_access_token(
        subject=str(user.id),
    )
