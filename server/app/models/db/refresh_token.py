from __future__ import annotations

import uuid
from datetime import UTC, datetime
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
        # A row is either explicitly revoked OR replaced via rotation, never both
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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user: Mapped["User"] = relationship(
        lazy="raise"
    )  # prevent accidentally accessing .user

    # Public lookup key sent as the first half of the client-facing token
    selector: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    # The second part of the token
    verifier_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

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

    # Set only for explicit revocation, NOT for normal rotation
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    replaced_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("refresh_tokens.id", ondelete="SET NULL"),
        nullable=True,
    )

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(UTC)

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_replaced(self) -> bool:
        return self.replaced_by is not None

    def is_valid(self) -> bool:
        return (
            not self.is_expired() and not self.is_revoked() and not self.is_replaced()
        )
