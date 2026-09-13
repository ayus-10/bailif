import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.db import Project


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    public_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1000, increment=1),
        unique=True,
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Core attributes
    # ------------------------------------------------------------------
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    # ------------------------------------------------------------------
    # Soft deletion
    # ------------------------------------------------------------------
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # only admin-initiated deletions set this
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ------------------------------------------------------------------
    # Project state
    # ------------------------------------------------------------------
    active_project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "projects.id",
            use_alter=True,
            name="fk_users_active_project_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    projects: Mapped[list["Project"]] = relationship(
        back_populates="user",
        foreign_keys="Project.user_id",
        lazy="raise",
    )

    # Exception to the lazy="raise" default
    active_project: Mapped["Project | None"] = relationship(
        foreign_keys="User.active_project_id",
        lazy="joined",
    )

    __table_args__ = (
        CheckConstraint(
            "length(username) >= 3",
            name="ck_users_username_min_length",
        ),
        CheckConstraint(
            "deleted_at IS NULL OR deleted_at >= created_at",
            name="ck_users_deleted_after_created",
        ),
        Index("ix_users_active_project_id", "active_project_id"),
        Index("ix_users_deleted_at", "deleted_at"),
        # Common "list active, non-deleted users" query
        Index("ix_users_is_active_deleted_at", "is_active", "deleted_at"),
    )

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_valid(self) -> bool:
        return self.is_active and not self.is_deleted()

    def soft_delete(self, *, deleted_by: uuid.UUID | None = None) -> None:
        self.deleted_at = datetime.now(UTC)
        self.deleted_by = deleted_by

    def restore(self) -> None:
        self.deleted_at = None
        self.deleted_by = None

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
