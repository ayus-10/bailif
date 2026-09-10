from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any, Callable

import jwt

from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# Bind tokens to this service so a JWT minted for one API can't be replayed
# against another that happens to share a secret store.
JWT_ISSUER = settings.jwt_issuer          # e.g. "myapp-auth"
JWT_AUDIENCE = settings.jwt_audience      # e.g. "myapp-api"

# Small tolerance for clock drift between servers verifying tokens.
CLOCK_SKEW_LEEWAY_SECONDS = 30


# ---------------------------------------------------------------------------
# Errors — callers should catch these, not PyJWT's exceptions directly.
# Keeps the JWT library an implementation detail instead of leaking into
# route handlers / middleware across the codebase.
# ---------------------------------------------------------------------------

class TokenError(Exception):
    """Base class for all token-related failures."""


class TokenExpiredError(TokenError):
    pass


class TokenInvalidError(TokenError):
    """Malformed, badly signed, wrong issuer/audience, or wrong type."""


# ---------------------------------------------------------------------------
# Secret key handling
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _get_secret_key() -> str:
    key = settings.jwt_secret_key
    if not key:
        raise RuntimeError(
            "JWT_SECRET_KEY is not set. Refusing to start — tokens must not "
            "be signed without a server-side secret."
        )
    if len(key) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be >=32 chars of random data.")
    return key


def validate_auth_settings() -> None:
    """
    Call once at app startup so misconfiguration fails fast at boot,
    not on the first request that happens to need a token.
    """
    _get_secret_key()
    _get_pepper()
    if not JWT_ISSUER or not JWT_AUDIENCE:
        raise RuntimeError("jwt_issuer and jwt_audience must both be set.")


# ---------------------------------------------------------------------------
# Low-level encode/decode
# ---------------------------------------------------------------------------

def encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)


def decode(token: str) -> dict[str, Any]:
    """
    Verify signature, issuer, audience, and required claims.
    Raises TokenExpiredError / TokenInvalidError instead of PyJWT's
    exceptions so callers don't need to import PyJWT.
    """
    try:
        return jwt.decode(
            token,
            _get_secret_key(),
            algorithms=[ALGORITHM],  # explicit whitelist — never trust the token's own `alg` header
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            leeway=CLOCK_SKEW_LEEWAY_SECONDS,
            options={"require": ["exp", "iat", "sub", "jti", "type"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        # Covers bad signature, wrong issuer/audience, malformed token,
        # missing required claims, etc.
        raise TokenInvalidError(str(exc)) from exc


# ---------------------------------------------------------------------------
# Access tokens
# ---------------------------------------------------------------------------

# Optional hook: plug in a Redis/DB check for "has this jti been revoked
# early?" (e.g. user logged out everywhere, or the token was flagged as
# stolen). Access tokens are normally left to just expire, but wiring this
# in gives you an emergency revocation path without waiting out the TTL.
# Leave as a no-op if you don't need it.
_jti_revocation_checker: Callable[[str], bool] | None = None


def set_jti_revocation_checker(checker: Callable[[str], bool] | None) -> None:
    """checker(jti) -> True if that specific token has been revoked early."""
    global _jti_revocation_checker
    _jti_revocation_checker = checker


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    if extra_claims:
        # Never let caller-supplied claims clobber the reserved ones above.
        reserved = payload.keys()
        payload.update({k: v for k, v in extra_claims.items() if k not in reserved})

    return encode(payload)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Use this (not the generic `decode`) for verifying access tokens on
    protected routes — it also checks the `type` claim so a token minted
    for some other purpose (password reset, email verification, etc., if
    you ever add those under the same secret) can't be used as an access
    token, and checks early-revocation if a checker is configured.
    """
    claims = decode(token)
    if claims.get("type") != "access":
        raise TokenInvalidError("Token is not an access token")

    if _jti_revocation_checker is not None and _jti_revocation_checker(claims["jti"]):
        raise TokenInvalidError("Token has been revoked")

    return claims


# ---------------------------------------------------------------------------
# Refresh tokens (unchanged from before — opaque, DB-tracked, not JWTs)
# ---------------------------------------------------------------------------

SELECTOR_BYTES = 12  # ~16 url-safe chars, plenty to avoid collisions
VERIFIER_BYTES = 32  # 256 bits of entropy for the actual secret


@lru_cache(maxsize=1)
def _get_pepper() -> bytes:
    pepper = settings.refresh_token_pepper
    if not pepper:
        raise RuntimeError("REFRESH_TOKEN_PEPPER is not set")
    if len(pepper) < 32:
        raise RuntimeError("REFRESH_TOKEN_PEPPER must be >=32 chars")
    return pepper.encode("utf-8")


@dataclass(frozen=True)
class IssuedRefreshToken:
    selector: str        # store in DB, plaintext, unique indexed column
    verifier_hash: str   # store in DB, this is what you persist for the secret half
    full_token: str      # send to the client (cookie). Never store this raw.


def generate_refresh_token() -> IssuedRefreshToken:
    """Generate a new refresh token. Call this at login / rotation time."""
    selector = secrets.token_urlsafe(SELECTOR_BYTES)
    verifier = secrets.token_urlsafe(VERIFIER_BYTES)
    return IssuedRefreshToken(
        selector=selector,
        verifier_hash=_hash_verifier(verifier),
        full_token=f"{selector}.{verifier}",
    )


def _hash_verifier(verifier: str) -> str:
    return hmac.new(_get_pepper(), verifier.encode("utf-8"), hashlib.sha256).hexdigest()


def split_token(token: str) -> tuple[str, str] | None:
    """Split a raw client-presented token into (selector, verifier)."""
    if not token or token.count(".") != 1:
        return None
    selector, verifier = token.split(".", 1)
    if not selector or not verifier:
        return None
    return selector, verifier


def validate_token(stored_verifier_hash: str, provided_token: str) -> bool:
    """
    Validate a client-presented token against the hash stored for the row
    you already looked up via `selector` (see usage below).
    """
    parsed = split_token(provided_token)
    if parsed is None:
        return False
    _, verifier = parsed
    computed_hash = _hash_verifier(verifier)
    return hmac.compare_digest(stored_verifier_hash, computed_hash)


# ---------------------------------------------------------------------------
# Usage in your auth service (pseudocode, not part of this module):
#
# At app startup:
#   validate_auth_settings()
#   set_jti_revocation_checker(my_redis_jti_checker)   # optional
#
# On protected routes:
#   try:
#       claims = decode_access_token(token)
#   except TokenExpiredError:
#       return 401, "token_expired"
#   except TokenInvalidError:
#       return 401, "token_invalid"
#
# On login / rotation:
#   issued = generate_refresh_token()
#   db.insert(
#       selector=issued.selector,
#       verifier_hash=issued.verifier_hash,
#       user_id=user.id,
#       expires_at=now() + timedelta(days=30),
#       revoked_at=None,
#   )
#   set_cookie("refresh_token", issued.full_token, httponly=True, secure=True,
#              samesite="Lax", max_age=30*24*3600)
#
# On refresh:
#   parsed = split_token(request.cookies.get("refresh_token"))
#   if parsed is None: reject()
#   selector, _ = parsed
#   row = db.get_by_selector(selector)          # O(1) indexed lookup
#   if row is None: reject()
#   if row.revoked_at is not None:
#       # reuse of a rotated/revoked token = compromise signal
#       db.revoke_all_tokens_for_user(row.user_id)
#       reject()
#   if row.expires_at < now(): reject()
#   if not validate_token(row.verifier_hash, provided_token): reject()
#   # success — rotate: issue new token, mark this row revoked, chain replaced_by
# ---------------------------------------------------------------------------
