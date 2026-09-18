from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums.project import ProjectStatus
from app.models.enums.task import TaskType
from app.shared.enums import AgentPermissionLevel, TaskPriority, TaskStatus


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: int
    name: str
    description: str
    icon: str
    color: str | None
    status: ProjectStatus

    start_date: datetime | None
    target_end_date: datetime | None
    actual_end_date: datetime | None
    timezone: str | None

    agent_enabled: bool
    default_agent_permission_level: AgentPermissionLevel
    # external_refs: dict

    created_at: datetime
    updated_at: datetime


class TaskRead(BaseModel):
    public_id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    type: TaskType
    tags: str
    project_public_id: int
    parent_public_id: int | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    start_date: datetime | None
    project: ProjectRead | None = None

    model_config = {"from_attributes": True}
