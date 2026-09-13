import uuid
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums.project import ProjectStatus
from app.models.enums.shared import AgentPermissionLevel

if TYPE_CHECKING:
    from app.models.db import Task, Taskboard, User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    slug: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1000, increment=1),
        unique=True,
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Core attributes
    # ------------------------------------------------------------------
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    icon: Mapped[str] = mapped_column(
        String(64), nullable=False, default="mdi-folder-outline"
    )
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status_enum"),
        nullable=False,
        default=ProjectStatus.ACTIVE,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Scheduling
    # ------------------------------------------------------------------
    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    target_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # ------------------------------------------------------------------
    # Soft deletion
    # ------------------------------------------------------------------
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    # ------------------------------------------------------------------
    # Agentic layer
    # ------------------------------------------------------------------
    agent_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    default_agent_permission_level: Mapped[AgentPermissionLevel] = mapped_column(
        Enum(
            AgentPermissionLevel,
            name="agent_permission_level_enum",
        ),
        nullable=False,
        default=AgentPermissionLevel.PROPOSE_ONLY,
    )
    agent_activity_log: Mapped[list[dict]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    # ------------------------------------------------------------------
    # Integrations
    # ------------------------------------------------------------------
    external_refs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        lazy="raise",
    )
    taskboards: Mapped[list["Taskboard"]] = relationship(
        back_populates="project",
        lazy="raise",
    )
    # Exception to the lazy="raise" default
    user: Mapped["User"] = relationship(
        foreign_keys="Project.user_id",
        back_populates="projects",
        lazy="joined",
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        #  Temporal ordering
        CheckConstraint(
            "start_date IS NULL OR target_end_date IS NULL OR target_end_date >= start_date",
            name="ck_projects_target_end_after_start",
        ),
        CheckConstraint(
            "start_date IS NULL OR actual_end_date IS NULL OR actual_end_date >= start_date",
            name="ck_projects_actual_end_after_start",
        ),
        CheckConstraint(
            "deleted_at IS NULL OR deleted_at >= created_at",
            name="ck_projects_deleted_after_created",
        ),
        # Strategic composite indexes
        Index("ix_projects_user_status", "user_id", "status"),
        Index("ix_projects_deleted_at", "deleted_at"),
        Index("ix_projects_user_deleted_at", "user_id", "deleted_at"),
    )

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_overdue(self, *, now: datetime | None = None) -> bool:
        if self.target_end_date is None or self.is_deleted():
            return False
        reference = now or datetime.now(UTC)
        return self.actual_end_date is None and self.target_end_date < reference

    def duration_days(self) -> int | None:
        if self.start_date is None or self.actual_end_date is None:
            return None
        return (self.actual_end_date - self.start_date) // timedelta(days=1)

    def soft_delete(self, *, deleted_by: uuid.UUID | None = None) -> None:
        self.deleted_at = datetime.now(UTC)
        self.deleted_by = deleted_by

    def restore(self) -> None:
        self.deleted_at = None
        self.deleted_by = None
