from datetime import datetime, timezone

from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.core.security.jwt as tokens
from app.core.exceptions import InternalServerError
from app.features.auth.constants import DUMMY_PASSWORD_HASH
from app.features.auth.exceptions import InvalidCredentialsError
from app.models.db.refresh_token import RefreshToken
from app.models.db.user import User

password_hasher = PasswordHash.recommended()


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = db.scalar(select(User).where(User.username == username))

    stored_hash = user.password_hash if user is not None else DUMMY_PASSWORD_HASH

    try:
        valid = password_hasher.verify(password, stored_hash)
    except UnknownHashError as exc:
        raise InternalServerError() from exc

    if user is None or not valid:
        raise InvalidCredentialsError()

    return user


def generate_access_token(user: User) -> str:
    return tokens.create_access_token(
        subject=str(user.id),
    )


def refresh_access_token(
    db: Session,
    refresh_token: str,
) -> str:
    """
    Validate and rotate a refresh token, then issue a new access token.
    """

    # 1. Parse + cryptographically validate the opaque token.
    token_data = tokens.validate_token(refresh_token)

    # token_data should contain at least:
    # - selector
    # - verifier_hash / equivalent validated data

    # 2. Find the DB record using the selector.
    stored_token = db.scalar(
        select(RefreshToken).where(RefreshToken.selector == token_data.selector)
    )

    if stored_token is None:
        raise InvalidCredentialsError()

    # 3. Check DB-side revocation / expiry.
    now = datetime.now(timezone.utc)

    if stored_token.revoked_at is not None:
        raise InvalidCredentialsError()

    if stored_token.expires_at <= now:
        raise InvalidCredentialsError()

    # 4. Verify the supplied verifier against the stored HMAC hash.
    if not tokens.verify_token(
        refresh_token,
        stored_token.verifier_hash,
    ):
        raise InvalidCredentialsError()

    # 5. Revoke the old refresh token.
    stored_token.revoked_at = now

    # 6. Generate a completely new refresh token.
    issued = tokens.generate_refresh_token()

    new_token = RefreshToken(
        selector=issued.selector,
        verifier_hash=issued.verifier_hash,
        user_id=stored_token.user_id,
        expires_at=issued.expires_at,
    )

    db.add(new_token)

    # 7. Issue a new short-lived access token.
    access_token = tokens.create_access_token(
        subject=str(stored_token.user_id),
    )

    db.commit()

    return access_token


def logout(
    db: Session,
    refresh_token: str,
) -> None:
    """
    Revoke the supplied refresh token.

    Logout is intentionally idempotent: if the token does not exist
    or has already been revoked, there is nothing else to do.
    """

    token_data = tokens.validate_token(refresh_token)

    stored_token = db.scalar(
        select(RefreshToken).where(RefreshToken.selector == token_data.selector)
    )

    if stored_token is None:
        return

    if stored_token.revoked_at is not None:
        return

    # Verify the actual verifier before revoking anything.
    if not tokens.verify_token(
        refresh_token,
        stored_token.verifier_hash,
    ):
        return

    stored_token.revoked_at = datetime.now(timezone.utc)

    db.commit()


def logout_all(
    db: Session,
    user: User,
) -> None:
    """
    Revoke every active refresh token belonging to the user.

    Existing access JWTs are not revoked here; they remain valid until
    their normal expiration.
    """

    now = datetime.now(timezone.utc)

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked_at.is_(None),
    ).update(
        {
            RefreshToken.revoked_at: now,
        },
        synchronize_session=False,
    )

    db.commit()
