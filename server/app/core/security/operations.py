import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from app.core.security.config import get_refresh_pepper
from app.core.security.constants import SELECTOR_BYTES, VERIFIER_BYTES
from app.core.security.schemas import IssuedRefreshToken


def issue_refresh_token() -> IssuedRefreshToken:
    selector = secrets.token_urlsafe(SELECTOR_BYTES)
    verifier = secrets.token_urlsafe(VERIFIER_BYTES)

    return IssuedRefreshToken(
        selector=selector,
        verifier_hash=_hash_verifier(verifier),
        full_token=f"{selector}.{verifier}",
        expires_at=datetime.now(UTC) + timedelta(minutes=15),
    )


def validate_refresh_token(
    stored_verifier_hash: str,
    expires_at: datetime,
    provided_token: str,
) -> bool:
    if datetime.now(UTC) >= expires_at:
        return False

    parsed = parse_refresh_token(provided_token)

    if parsed is None:
        return False

    _, verifier = parsed

    return hmac.compare_digest(
        stored_verifier_hash,
        _hash_verifier(verifier),
    )


def parse_refresh_token(token: str) -> tuple[str, str] | None:
    if not token or token.count(".") != 1:
        return None

    selector, verifier = token.split(".", 1)

    if not selector or not verifier:
        return None

    return selector, verifier


def _hash_verifier(verifier: str) -> str:
    return hmac.new(
        get_refresh_pepper(),
        verifier.encode(),
        hashlib.sha256,
    ).hexdigest()
