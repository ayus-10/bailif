import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    DateTime,
    ForeignKey,
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

    # Core attributes
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)

    # Project link
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True
    )
    project: Mapped[Project | None] = relationship(
        "Project", back_populates="taskboards", lazy="joined"
    )

    # Relationships
    task_associations: Mapped[list[TaskboardTask]] = relationship(
        "TaskboardTask",
        back_populates="taskboard",
        cascade="all, delete-orphan",
        foreign_keys="TaskboardTask.taskboard_id",
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task",
        secondary="taskboard_tasks",
        viewonly=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TaskboardTask(Base):
    __tablename__ = "taskboard_tasks"

    # Core attributes
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    taskboard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("taskboards.id", ondelete="CASCADE"),
        nullable=False,
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    position: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    taskboard: Mapped[Taskboard] = relationship(
        "Taskboard", back_populates="task_associations", lazy="joined"
    )
    task: Mapped[Task] = relationship(lazy="joined")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("taskboard_id", "task_id", name="uq_taskboard_task"),
    )
