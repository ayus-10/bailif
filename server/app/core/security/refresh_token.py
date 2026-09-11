import hashlib
import hmac
import secrets
from dataclasses import dataclass

from app.core.security.config import get_refresh_pepper

SELECTOR_BYTES = 12
VERIFIER_BYTES = 32


@dataclass(frozen=True)
class IssuedRefreshToken:
    selector: str
    verifier_hash: str
    full_token: str


def generate_refresh_token() -> IssuedRefreshToken:
    selector = secrets.token_urlsafe(SELECTOR_BYTES)
    verifier = secrets.token_urlsafe(VERIFIER_BYTES)

    return IssuedRefreshToken(
        selector=selector,
        verifier_hash=_hash_verifier(verifier),
        full_token=f"{selector}.{verifier}",
    )


def _hash_verifier(verifier: str) -> str:
    return hmac.new(
        get_refresh_pepper(),
        verifier.encode(),
        hashlib.sha256,
    ).hexdigest()


def split_token(token: str) -> tuple[str, str] | None:
    if not token or token.count(".") != 1:
        return None

    selector, verifier = token.split(".", 1)

    if not selector or not verifier:
        return None

    return selector, verifier


def validate_token(
    stored_verifier_hash: str,
    provided_token: str,
) -> bool:
    parsed = split_token(provided_token)

    if parsed is None:
        return False

    _, verifier = parsed

    return hmac.compare_digest(
        stored_verifier_hash,
        _hash_verifier(verifier),
    )
