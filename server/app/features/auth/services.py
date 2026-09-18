from datetime import UTC, datetime
from uuid import UUID

from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import InternalServerError
from app.core.security.jwt import create_access_token
from app.core.security.operations import (
    issue_refresh_token,
    parse_refresh_token,
    validate_refresh_token,
)
from app.features.auth.constants import DUMMY_PASSWORD_HASH, MAX_SELECTOR_RETRIES
from app.features.auth.exceptions import (
    InvalidCredentialsError,
    RefreshTokenIssuanceError,
)
from app.models.db import RefreshToken, User

password_hasher = PasswordHash.recommended()


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = db.scalar(select(User).where(User.username == username))

    stored_hash = user.password_hash if user is not None else DUMMY_PASSWORD_HASH

    try:
        is_password_correct = password_hasher.verify(password, stored_hash)
    except UnknownHashError as exc:
        raise InternalServerError("Unable to verify the provided password.") from exc

    if user is None or not is_password_correct or not user.is_valid():
        raise InvalidCredentialsError("Invalid username or password.")

    return user


def generate_access_token(user: User) -> str:
    return create_access_token(
        subject=str(user.id),
    )


def generate_refresh_token(
    db: Session,
    user: User,
    *,
    user_agent: str | None,
    ip_address: str | None,
) -> str:
    for _ in range(MAX_SELECTOR_RETRIES):
        issued_token = issue_refresh_token()

        refresh_token = RefreshToken(
            user_id=user.id,
            selector=issued_token.selector,
            verifier_hash=issued_token.verifier_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=issued_token.expires_at,
        )

        try:
            with db.begin_nested():
                db.add(refresh_token)
                db.flush()
        except IntegrityError:
            continue
        else:
            return issued_token.full_token

    raise RefreshTokenIssuanceError(
        "Failed to generate a unique refresh token selector"
    )


def redeem_refresh_token(
    db: Session,
    refresh_token: str,
    *,
    user_agent: str | None,
    ip_address: str | None,
) -> tuple[str, str]:
    stored_token = _find_stored_token_by_raw(db, refresh_token)

    if stored_token is None:
        raise InvalidCredentialsError("Invalid or expired refresh token.")

    now = datetime.now(UTC)

    if not validate_refresh_token(
        stored_token.verifier_hash,
        stored_token.expires_at,
        refresh_token,
    ):
        raise InvalidCredentialsError("Invalid or expired refresh token.")

    if stored_token.revoked_at is not None:
        _revoke_all_tokens_for_user(db, stored_token.user_id)
        db.commit()
        raise InvalidCredentialsError("Refresh token has already been used.")

    user = db.scalar(select(User).where(User.id == stored_token.user_id))

    if user is None or not user.is_valid():
        _revoke_all_tokens_for_user(db, stored_token.user_id)
        db.commit()
        raise InvalidCredentialsError("Invalid or expired refresh token.")

    stored_token.revoked_at = now

    issued = issue_refresh_token()

    new_token = RefreshToken(
        user_id=stored_token.user_id,
        selector=issued.selector,
        verifier_hash=issued.verifier_hash,
        user_agent=stored_token.user_agent if user_agent is None else user_agent,
        ip_address=stored_token.ip_address if ip_address is None else ip_address,
        expires_at=issued.expires_at,
    )

    db.add(new_token)

    access_token = create_access_token(
        subject=str(stored_token.user_id),
    )

    return access_token, issued.full_token


def logout(db: Session, refresh_token: str) -> None:
    stored_token = _find_stored_token_by_raw(db, refresh_token)

    if stored_token is None:
        return

    if stored_token.revoked_at is not None:
        return

    if not validate_refresh_token(
        stored_token.verifier_hash,
        stored_token.expires_at,
        refresh_token,
    ):
        return

    user = db.scalar(select(User).where(User.id == stored_token.user_id))

    if user is None or not user.is_valid():
        return

    stored_token.revoked_at = datetime.now(UTC)


def logout_all(
    db: Session,
    user: User,
) -> None:
    now = datetime.now(UTC)

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked_at.is_(None),
    ).update(
        {
            RefreshToken.revoked_at: now,
        },
        synchronize_session=False,
    )


def _revoke_all_tokens_for_user(
    db: Session,
    user_id: UUID,
) -> None:
    now = datetime.now(UTC)

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None),
    ).update(
        {
            RefreshToken.revoked_at: now,
        },
        synchronize_session=False,
    )


def _find_stored_token_by_raw(
    db: Session,
    raw_token: str,
) -> RefreshToken | None:
    parsed = parse_refresh_token(raw_token)

    if parsed is None:
        return None

    selector, _ = parsed

    return db.scalar(select(RefreshToken).where(RefreshToken.selector == selector))
