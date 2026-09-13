import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    UUID,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.agent.schemas.enums import ActionStatus
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.db import Project, User


class Action(Base):
    __tablename__ = "actions"

    __table_args__ = (
        CheckConstraint(
            "expires_at > created_at",
            name="ck_actions_expires_after_created",
        ),
        CheckConstraint(
            "(status = 'confirmed') = (confirmed_at IS NOT NULL)",
            name="ck_actions_confirmed_state",
        ),
        Index(
            "ix_actions_user_status_created",
            "user_id",
            "status",
            "created_at",
        ),
        Index(
            "ix_actions_project_status_created",
            "project_id",
            "status",
            "created_at",
        ),
        Index(
            "ix_actions_expires_at",
            "expires_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            name="fk_actions_user_id",
        ),
        nullable=False,
    )

    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
            name="fk_actions_project_id",
        ),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------
    prompt: Mapped[str] = mapped_column(
        String(10_000),
        nullable=False,
    )

    reply: Mapped[str] = mapped_column(
        String(50_000),
        nullable=False,
    )

    # Structured backend execution plan
    plan: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------
    status: Mapped[ActionStatus] = mapped_column(
        String(20),
        nullable=False,
        default=ActionStatus.PENDING,
        server_default=ActionStatus.PENDING.value,
    )

    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        lazy="raise",
    )

    project: Mapped["Project | None"] = relationship(
        foreign_keys=[project_id],
        lazy="raise",
    )

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------
    def is_completed(self) -> bool:
        return self.status == ActionStatus.COMPLETED

    def is_terminal(self) -> bool:
        return self.status in {
            ActionStatus.COMPLETED,
            ActionStatus.REJECTED,
            ActionStatus.PARTIALLY_FAILED,
            ActionStatus.FAILED,
        }

    def is_expired(self, *, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        return now >= self.expires_at

    def can_complete(self, *, now: datetime | None = None) -> bool:
        return self.status == ActionStatus.PENDING and not self.is_expired(now=now)

    def complete(self, *, at: datetime | None = None) -> None:
        if not self.can_complete(now=at):
            raise ValueError("Action cannot be completed.")

        completed_at = at or datetime.now(UTC)

        self.status = ActionStatus.COMPLETED
        self.completed_at = completed_at

    def reject(self) -> None:
        if self.status != ActionStatus.PENDING:
            raise ValueError("Only pending actions can be rejected.")

        self.status = ActionStatus.REJECTED

    def mark_partially_failed(self) -> None:
        if self.status != ActionStatus.PENDING:
            raise ValueError("Only pending actions can be marked as partially failed.")

        self.status = ActionStatus.PARTIALLY_FAILED

    def mark_failed(self) -> None:
        if self.status != ActionStatus.PENDING:
            raise ValueError("Only pending actions can be marked as failed.")

        self.status = ActionStatus.FAILED
