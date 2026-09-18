import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    UUID,
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums.task import (
    EdgeType,
    TaskType,
)
from app.shared.constants import TASK_STATUS_TRANSITIONS
from app.shared.enums import (
    AgentPermissionLevel,
    ApprovalStatus,
    CreatedBy,
    TaskPriority,
    TaskStatus,
)

if TYPE_CHECKING:
    from app.models.db import Project


EMBEDDING_DIM = 2560


class Task(Base):
    __tablename__ = "tasks"

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
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="status_enum"),
        nullable=False,
        default=TaskStatus.OPEN,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, name="priority_enum"),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    type: Mapped[TaskType] = mapped_column(
        Enum(TaskType, name="task_type_enum"),
        nullable=False,
        default=TaskType.TASK,
    )
    tags: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # ------------------------------------------------------------------
    # Scheduling
    # ------------------------------------------------------------------
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

    # Soft deletion
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    # ------------------------------------------------------------------
    # Hierarchy / edges
    # ------------------------------------------------------------------
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    subtasks: Mapped[list["Task"]] = relationship(
        back_populates="parent",
        lazy="raise",
    )
    parent: Mapped["Task | None"] = relationship(
        back_populates="subtasks",
        remote_side="Task.id",
        lazy="raise",
    )
    outgoing_edges: Mapped[list["TaskEdge"]] = relationship(
        foreign_keys="TaskEdge.task_id",
        back_populates="task",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    incoming_edges: Mapped[list["TaskEdge"]] = relationship(
        foreign_keys="TaskEdge.depends_on_id",
        back_populates="depends_on",
        lazy="raise",
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Almost every Task read is "give me the task and its project"
    # so eager-loading by default here is a deliberate
    project: Mapped["Project"] = relationship(
        back_populates="tasks",
        lazy="joined",
    )

    # ------------------------------------------------------------------
    # Agentic layer
    # ------------------------------------------------------------------
    created_by: Mapped[CreatedBy] = mapped_column(
        Enum(CreatedBy, name="created_by_enum"),
        nullable=False,
        default=CreatedBy.HUMAN,
    )
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus, name="approval_status_enum"),
        nullable=False,
        default=ApprovalStatus.NONE,
    )
    agent_permission_level: Mapped[AgentPermissionLevel | None] = mapped_column(
        Enum(AgentPermissionLevel, name="agent_permission_level_enum"),
        nullable=True,
    )
    agent_activity_log: Mapped[list[dict]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    reasoning_trace: Mapped[str | None] = mapped_column(Text, nullable=True)

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIM), nullable=True
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
        # Temporal ordering
        CheckConstraint(
            "start_date IS NULL OR due_date IS NULL OR due_date > start_date",
            name="ck_tasks_due_after_start",
        ),
        CheckConstraint(
            "deleted_at IS NULL OR deleted_at >= created_at",
            name="ck_tasks_deleted_after_created",
        ),
        # Cross-field relationships
        CheckConstraint(
            "created_by <> 'AGENT' OR agent_permission_level IS NOT NULL",
            name="ck_tasks_agent_requires_permission_level",
        ),
        CheckConstraint(
            "created_by <> 'AGENT' OR status <> 'DONE' OR approval_status = 'APPROVED'",
            name="ck_tasks_agent_completion_requires_approval",
        ),
        # Strategic composite indexes
        Index(
            "ix_tasks_project_status_created_at",
            "project_id",
            "status",
            "created_at",
        ),
        Index(
            "ix_tasks_project_due_date",
            "project_id",
            "due_date",
        ),
        Index("ix_tasks_deleted_at", "deleted_at"),
        Index(
            "ix_tasks_project_deleted_at",
            "project_id",
            "deleted_at",
        ),
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

    def is_overdue(self, *, now: datetime | None = None) -> bool:
        if self.due_date is None or self.is_deleted():
            return False
        reference = now or datetime.now(UTC)
        return self.due_date < reference and not self.is_terminal()

    def is_terminal(self) -> bool:
        return self.status in (TaskStatus.DONE, TaskStatus.CANCELLED)

    def can_transition_to(self, new_status: "TaskStatus") -> bool:
        if self.is_deleted():
            return False
        if new_status not in TASK_STATUS_TRANSITIONS.get(self.status, set()):
            return False
        return True

    def has_unresolved_blocking_edges(self) -> bool:
        return any(
            dep.edge_type == EdgeType.BLOCKS and dep.task.status != TaskStatus.DONE
            for dep in self.incoming_edges
        )

    def is_awaiting_approval(self) -> bool:
        return self.approval_status == ApprovalStatus.PENDING

    def is_approved(self) -> bool:
        return self.approval_status == ApprovalStatus.APPROVED

    def is_rejected(self) -> bool:
        return self.approval_status == ApprovalStatus.REJECTED


class TaskEdge(Base):
    __tablename__ = "task_edges"

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

    edge_type: Mapped[EdgeType] = mapped_column(
        Enum(EdgeType, name="edge_type_enum"),
        nullable=False,
        default=EdgeType.BLOCKS,
    )

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False, index=True
    )
    depends_on_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    task: Mapped["Task"] = relationship(
        foreign_keys="TaskEdge.task_id",
        back_populates="outgoing_edges",
        lazy="raise",
    )
    depends_on: Mapped["Task"] = relationship(
        foreign_keys="TaskEdge.depends_on_id",
        back_populates="incoming_edges",
        lazy="raise",
    )

    __table_args__ = (
        CheckConstraint(
            "task_id <> depends_on_id",
            name="ck_task_edges_no_self_reference",
        ),
        UniqueConstraint(
            "task_id",
            "depends_on_id",
            "edge_type",
            name="uq_task_edge",
        ),
    )

    def is_self_referential(self) -> bool:
        return self.task_id == self.depends_on_id
