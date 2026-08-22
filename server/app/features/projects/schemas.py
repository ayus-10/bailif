import re
from datetime import datetime
from typing import Annotated
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.db.project import (
    AgentPermissionLevel,
    ProjectStatus,
)
from app.utils.date_validation import after


class ProjectFieldValidators(BaseModel):
    @field_validator("name", check_fields=False)
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty")
        return v

    @field_validator("description", check_fields=False)
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if len(v) > 5000:
            raise ValueError("description cannot exceed 5000 characters")
        return v

    @field_validator("color", check_fields=False)
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
            raise ValueError("color must be a valid hex color")
        return v

    @field_validator("timezone", check_fields=False)
    @classmethod
    def validate_timezone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            ZoneInfo(v)
        except ZoneInfoNotFoundError:
            raise ValueError("invalid timezone")
        return v


class ProjectCreate(ProjectFieldValidators):
    name: str = Field(min_length=1, max_length=500)
    description: str = ""
    icon: Annotated[str, Field(max_length=50)] = "mdi-folder-outline"
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
    # external_refs: dict = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_date_order(self: ProjectCreate):
        after(self.start_date, self.target_end_date)
        after(self.start_date, self.actual_end_date)
        return self


class ProjectUpdate(ProjectFieldValidators):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    description: str | None = None
    icon: Annotated[str, Field(max_length=50)] | None = None
    color: str | None = None
    status: ProjectStatus | None = None

    start_date: datetime | None = None
    target_end_date: datetime | None = None
    actual_end_date: datetime | None = None
    timezone: str | None = None

    agent_enabled: bool | None = None
    default_agent_permission_level: AgentPermissionLevel | None = None
    # external_refs: dict | None = None

    @model_validator(mode="after")
    def validate_date_order(self: ProjectUpdate):
        after(self.start_date, self.target_end_date)
        after(self.start_date, self.actual_end_date)
        return self


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
    # external_refs: dict

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
