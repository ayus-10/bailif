import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.enums.task import TaskType
from app.shared.enums import TaskPriority, TaskStatus
from app.shared.schemas import TaskRead
from app.utils.date_validation import validate_datetime_range


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
        if len(v) > 50000:
            raise ValueError("description cannot exceed 50000 characters")
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
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.MEDIUM
    type: TaskType = TaskType.TASK
    tags: str = ""
    parent_public_id: int | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None

    @model_validator(mode="after")
    def validate_date_order(self):
        validate_datetime_range(self.start_date, self.due_date)
        return self


class TaskUpdate(TaskFieldValidators):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    type: TaskType | None = None
    tags: str | None = None
    parent_public_id: int | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None

    @model_validator(mode="after")
    def validate_date_order(self):
        validate_datetime_range(self.start_date, self.due_date)
        return self


class TaskFilterParams(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    type: TaskType | None = None
    tag: str | None = None
    parent_public_id: int | None = None
    taskboard_public_id: int | None = None
    only_root: bool = False
    due_before: datetime | None = None
    due_after: datetime | None = None
    cursor: str | None = None
    limit: int = Field(default=50, ge=1, le=200)

    @model_validator(mode="after")
    def validate_parent_filters(self):
        if self.only_root and self.parent_public_id is not None:
            raise ValueError("only_root and parent_public_id cannot be used together")
        return self


class TaskListResponse(BaseModel):
    items: list[TaskRead]
    next_cursor: str | None = None
