import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.db import Project, Task


class Taskboard(Base):
    __tablename__ = "taskboards"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)

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
    # Project link
    # ------------------------------------------------------------------
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Exception to the lazy="raise" default
    project: Mapped["Project"] = relationship(
        back_populates="taskboards",
        lazy="joined",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    task_associations: Mapped[list["TaskboardTask"]] = relationship(
        back_populates="taskboard",
        cascade="all, delete-orphan",
        foreign_keys="TaskboardTask.taskboard_id",
        lazy="raise",
    )
    tasks: Mapped[list["Task"]] = relationship(
        secondary="taskboard_tasks",
        viewonly=True,
        lazy="raise",
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

    __table_args__ = (
        CheckConstraint(
            "deleted_at IS NULL OR deleted_at >= created_at",
            name="ck_taskboards_deleted_after_created",
        ),
        # Soft-delete filtering
        Index("ix_taskboards_deleted_at", "deleted_at"),
        Index("ix_taskboards_project_deleted_at", "project_id", "deleted_at"),
    )

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self, *, deleted_by: uuid.UUID | None = None) -> None:
        self.deleted_at = datetime.now(UTC)
        self.deleted_by = deleted_by

    def restore(self) -> None:
        self.deleted_at = None
        self.deleted_by = None


class TaskboardTask(Base):
    __tablename__ = "taskboard_tasks"

    # ------------------------------------------------------------------
    # Core attributes
    # ------------------------------------------------------------------
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    taskboard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("taskboards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    taskboard: Mapped["Taskboard"] = relationship(
        back_populates="task_associations",
        lazy="raise",
    )
    # Exception to the lazy="raise" default
    task: Mapped["Task"] = relationship(lazy="joined")

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
        UniqueConstraint("taskboard_id", "task_id", name="uq_taskboard_task"),
        CheckConstraint(
            "position >= 0", name="ck_taskboard_tasks_position_non_negative"
        ),
        # Two cards can't sit at the same position on the same board. This
        # is DEFERRABLE INITIALLY DEFERRED because reordering legitimately
        # produces a transient duplicate mid-transaction.
        UniqueConstraint(
            "taskboard_id",
            "position",
            name="uq_taskboard_tasks_position",
            deferrable=True,
            initially="DEFERRED",
        ),
    )
