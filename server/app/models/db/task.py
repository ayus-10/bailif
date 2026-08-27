import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import UUID, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums.shared import (
    AgentPermissionLevel,
    ApprovalStatus,
    CreatedBy,
    TaskPriority,
    TaskStatus,
)
from app.models.enums.task import (
    DependencyType,
    TaskType,
)

if TYPE_CHECKING:
    from app.models.db.project import Project


EMBEDDING_DIM = 2560


class Task(Base):
    __tablename__ = "tasks"

    # Core attributes
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="status_enum"),
        default=TaskStatus.OPEN,
        nullable=False,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, name="priority_enum"),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    type: Mapped[TaskType] = mapped_column(
        Enum(TaskType, name="task_type_enum"),
        default=TaskType.TASK,
        nullable=False,
    )
    tags: Mapped[str] = mapped_column(String(255), default="")

    # Scheduling
    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    recurrence_rule: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # RRULE string, e.g. "FREQ=WEEKLY;BYDAY=MO"

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    subtasks: Mapped[list["Task"]] = relationship(
        back_populates="parent",
    )
    parent: Mapped["Task | None"] = relationship(
        back_populates="subtasks",
        remote_side="Task.id",
    )

    outgoing_dependencies: Mapped[list[TaskDependency]] = relationship(
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    # Project link
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    project: Mapped[Project] = relationship(back_populates="tasks")

    # Agentic layer
    created_by: Mapped[CreatedBy] = mapped_column(
        Enum(CreatedBy, name="created_by_enum"),
        default=CreatedBy.HUMAN,
        nullable=False,
    )
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus, name="approval_status_enum"),
        default=ApprovalStatus.NONE,
        nullable=False,
    )
    agent_permission_level: Mapped[AgentPermissionLevel | None] = mapped_column(
        Enum(AgentPermissionLevel, name="agent_permission_level_enum"),
        nullable=True,
    )
    agent_activity_log: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    reasoning_trace: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Embedding
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIM), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TaskDependency(Base):
    """
    Typed edge between two tasks. dependency_type is stored from the perspective of `task_id`
    e.g. task_id="blocks" depends_on_id means task_id blocks depends_on_id.
    """

    __tablename__ = "task_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    dependency_type: Mapped[DependencyType] = mapped_column(
        Enum(DependencyType, name="dependency_type_enum"),
        default=DependencyType.BLOCKS,
        nullable=False,
    )

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id")
    )
    depends_on_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id")
    )

    task: Mapped["Task"] = relationship(
        foreign_keys="TaskDependency.task_id",
        back_populates="outgoing_dependencies",
    )
    depends_on: Mapped["Task"] = relationship(
        foreign_keys="TaskDependency.depends_on_id",
        back_populates="incoming_dependencies",
    )
