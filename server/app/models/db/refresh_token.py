from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.db import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        # A row is either explicitly revoked (logout, theft response) OR
        # replaced via rotation — never both. Rotation code must set only
        # `replaced_by`, not `revoked_at`, when a token is superseded.
        CheckConstraint(
            "NOT (revoked_at IS NOT NULL AND replaced_by IS NOT NULL)",
            name="ck_revoked_xor_replaced",
        ),
        CheckConstraint(
            "expires_at > created_at",
            name="ck_expires_after_created",
        ),
        Index("ix_refresh_tokens_user_id_expires_at", "user_id", "expires_at"),
        Index("ix_refresh_tokens_user_id_revoked_at", "user_id", "revoked_at"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # lazy="raise": touching .user on a hot auth-check path should be a
    # deliberate decision, not an accidental implicit query.
    user: Mapped["User"] = relationship(lazy="raise")

    # Public lookup key sent as the first half of the client-facing token
    # ("selector.verifier"). Plaintext in DB — it's useless without the
    # verifier, and having it plaintext is what makes the DB lookup O(1)
    # instead of scanning/hashing every row.
    selector: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    # HMAC-SHA256(pepper, verifier) — hex digest is always 64 chars.
    verifier_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    # Headers aren't guaranteed present (proxies strip them, some clients
    # omit them) — don't hard-fail an otherwise valid login over it.
    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),  # IPv4 (15) + IPv6 (39) + buffer
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Set only for explicit revocation events (logout, logout-all, theft
    # detection response) — NOT for normal rotation. See check constraint.
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Points to the token that superseded this one via rotation. Presence
    # of this alone means "no longer usable" — don't also set revoked_at.
    replaced_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("refresh_tokens.id", ondelete="SET NULL"),
        nullable=True,
    )

    def is_expired(self) -> bool:
        """Check if the token has passed its expiration time."""
        return self.expires_at <= datetime.now(timezone.utc)

    def is_revoked(self) -> bool:
        """Check if the token was explicitly revoked."""
        return self.revoked_at is not None

    def is_replaced(self) -> bool:
        """Check if the token was replaced during rotation."""
        return self.replaced_by is not None

    def is_valid(self) -> bool:
        """Check if the token is currently valid (not expired, revoked, or replaced)."""
        return not self.is_expired() and not self.is_revoked() and not self.is_replaced()
