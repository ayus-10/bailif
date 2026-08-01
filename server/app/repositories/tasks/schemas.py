from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.enums.shared import Priority, Status
from app.models.enums.task import TaskType


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
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

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.due_date is not None
            and self.start_date > self.due_date
        ):
            raise ValueError("start_date cannot be after due_date")

        return self


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
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

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, v: str | None) -> str | None:
        return v.strip() if v is not None else v

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.due_date is not None
            and self.start_date > self.due_date
        ):
            raise ValueError("start_date cannot be after due_date")

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
