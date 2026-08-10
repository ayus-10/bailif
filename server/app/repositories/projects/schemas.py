from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.db.project import (
    AgentPermissionLevel,
    ProjectStatus,
)


class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    icon: str = "mdi-folder-outline"
    color: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE

    start_date: datetime | None = None
    target_end_date: datetime | None = None
    actual_end_date: datetime | None = None
    timezone: str | None = None

    agent_enabled: bool = True
    default_agent_permission_level: AgentPermissionLevel = (
        AgentPermissionLevel.PROPOSE_ONLY
    )
    external_refs: dict = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    color: str | None = None
    status: ProjectStatus | None = None

    start_date: datetime | None = None
    target_end_date: datetime | None = None
    actual_end_date: datetime | None = None
    timezone: str | None = None

    agent_enabled: bool | None = None
    default_agent_permission_level: AgentPermissionLevel | None = None
    external_refs: dict | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        return v.strip()


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
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
    external_refs: dict

    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None


class ProjectFilterParams(BaseModel):
    status: ProjectStatus | None = None
    agent_enabled: bool | None = None
    start_date_before: datetime | None = None
    start_date_after: datetime | None = None
    target_end_date_before: datetime | None = None
    target_end_date_after: datetime | None = None
    archived: bool = False


class ProjectListResponse(BaseModel):
    items: list[ProjectRead]
