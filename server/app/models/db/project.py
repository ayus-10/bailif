import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums.project import ProjectStatus
from app.models.enums.shared import AgentPermissionLevel

if TYPE_CHECKING:
    from app.models.db import Task, Taskboard


class Project(Base):
    __tablename__ = "projects"

    # Core attributes
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    icon: Mapped[str] = mapped_column(String(64), default="mdi-folder-outline")
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status_enum"),
        default=ProjectStatus.ACTIVE,
        nullable=False,
    )

    # Scheduling
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

    # Agentic layer
    agent_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    default_agent_permission_level: Mapped[AgentPermissionLevel] = mapped_column(
        Enum(
            AgentPermissionLevel,
            name="agent_permission_level_enum",
        ),
        default=AgentPermissionLevel.PROPOSE_ONLY,
        nullable=False,
    )
    agent_activity_log: Mapped[list[dict]] = mapped_column(JSONB, default=list)

    # Integrations
    external_refs: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relations
    tasks: Mapped[list[Task]] = relationship("Task", back_populates="project")
    taskboards: Mapped[list[Taskboard]] = relationship("Taskboard", back_populates="project")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
