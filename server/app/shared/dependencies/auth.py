from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security.exceptions import TokenExpiredError, TokenInvalidError
from app.core.security.jwt import decode
from app.models.db.user import User
from app.shared.constants import TokenType
from app.shared.exceptions import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode(token)
    except TokenExpiredError as exc:
        raise AccessTokenExpiredError("Access token has expired") from exc
    except TokenInvalidError as exc:
        raise AccessTokenInvalidError("Invalid access token") from exc

    try:
        if payload["type"] != TokenType.ACCESS:
            raise AccessTokenInvalidError("Token is not an access token")

        user_id = UUID(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise AccessTokenInvalidError("Invalid access token payload") from exc

    user = db.scalar(
        select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
            User.is_active.is_(True),
        )
    )

    # TODO: user.active_project is lazy joined but nobody checked if the project is softdeleted

    if user is None:
        raise AccessTokenInvalidError("Invalid access token")

    return user
