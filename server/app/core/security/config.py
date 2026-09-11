from functools import lru_cache

from app.core.config import settings


@lru_cache(maxsize=1)
def get_jwt_secret() -> str:
    key = settings.jwt_secret_key
    if not key:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    if len(key) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be >=32 chars")
    return key


@lru_cache(maxsize=1)
def get_refresh_pepper() -> bytes:
    pepper = settings.refresh_token_pepper
    if not pepper:
        raise RuntimeError("REFRESH_TOKEN_PEPPER is not set")
    if len(pepper) < 32:
        raise RuntimeError("REFRESH_TOKEN_PEPPER must be >=32 chars")
    return pepper.encode()


def validate_auth_settings() -> None:
    get_jwt_secret()
    get_refresh_pepper()

    if not settings.jwt_issuer:
        raise RuntimeError("JWT_ISSUER is not set")

    if not settings.jwt_audience:
        raise RuntimeError("JWT_AUDIENCE is not set")
