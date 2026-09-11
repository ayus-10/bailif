from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt

from app.core.config import settings
from app.core.security.config import get_jwt_secret
from app.core.security.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    CLOCK_SKEW_LEEWAY_SECONDS,
)
from app.core.security.exceptions import TokenExpiredError, TokenInvalidError


def encode(payload: dict[str, Any]) -> str:
    return jwt.encode(
        payload,
        get_jwt_secret(),
        algorithm=ALGORITHM,
    )


def decode(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=[ALGORITHM],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            leeway=CLOCK_SKEW_LEEWAY_SECONDS,
            options={"require": ["exp", "iat", "sub", "jti", "type"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise TokenInvalidError(str(exc)) from exc


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "jti": str(uuid4()),
        "type": "access",
    }

    if extra_claims:
        payload.update({k: v for k, v in extra_claims.items() if k not in payload})

    return encode(payload)
