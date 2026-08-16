import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.enums.shared import Priority, Status
from app.models.enums.task import TaskType
from app.repositories.projects.schemas import ProjectRead
from app.utils.date_validation import after


class TaskFieldValidators(BaseModel):
    @field_validator("title", check_fields=False)
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
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

    @field_validator("tags", check_fields=False)
    @classmethod
    def validate_tags(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.fullmatch(r"[A-Za-z0-9 ,]*", v):
            raise ValueError("tags may only contain alphanumeric characters")
        tags = [tag.strip() for tag in v.split(",") if tag.strip()]
        return ",".join(tags)


class TaskCreate(TaskFieldValidators):
    title: str = Field(min_length=1, max_length=500)
    description: str = ""
    status: Status = Status.OPEN
    priority: Priority = Priority.MEDIUM
    type: TaskType = TaskType.TASK
    tags: str = ""
    project_id: UUID | None = None
    parent_id: UUID | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    estimated_duration_minutes: int | None = Field(
        default=None,
        ge=1,
    )

    @model_validator(mode="after")
    def validate_date_order(self):
        after(self.start_date, self.due_date)
        return self


class TaskUpdate(TaskFieldValidators):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    type: TaskType | None = None
    tags: str | None = None
    project_id: UUID | None = None
    parent_id: UUID | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    estimated_duration_minutes: int | None = Field(
        default=None,
        ge=1,
    )

    @model_validator(mode="after")
    def validate_date_order(self):
        after(self.start_date, self.due_date)
        return self


class TaskRead(BaseModel):
    id: UUID
    title: str
    description: str
    status: Status
    priority: Priority
    type: TaskType
    tags: str
    project_id: UUID | None
    parent_id: UUID | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    start_date: datetime | None
    estimated_duration_minutes: int | None
    project: ProjectRead | None = None

    model_config = {"from_attributes": True}


class TaskFilterParams(BaseModel):
    project_id: UUID | None = None
    status: Status | None = None
    priority: Priority | None = None
    type: TaskType | None = None
    tag: str | None = None
    parent_id: UUID | None = None
    due_before: datetime | None = None
    due_after: datetime | None = None
    cursor: str | None = None
    limit: int = Field(default=50, ge=1, le=200)


class TaskListResponse(BaseModel):
    items: list[TaskRead]
    next_cursor: str | None = None
