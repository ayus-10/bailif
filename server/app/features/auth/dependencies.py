from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.tokens import decode
from app.features.auth.exceptions import InvalidCredentialsError
from app.models.db.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode(token)
        user_id = UUID(payload["sub"])
    except jwt.InvalidTokenError, KeyError, ValueError:
        raise InvalidCredentialsError()

    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise InvalidCredentialsError()

    return user
