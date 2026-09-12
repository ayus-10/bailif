from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import TokenType
from app.core.database import get_db
from app.core.security.exceptions import TokenExpiredError, TokenInvalidError
from app.core.security.jwt import decode
from app.features.auth.exceptions import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
)
from app.models.db.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode(token)
    except TokenExpiredError as exc:
        raise AccessTokenExpiredError() from exc
    except TokenInvalidError as exc:
        raise AccessTokenInvalidError() from exc

    try:
        if payload["type"] != TokenType.ACCESS:
            raise AccessTokenInvalidError()

        user_id = UUID(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise AccessTokenInvalidError() from exc

    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise AccessTokenInvalidError()

    return user
