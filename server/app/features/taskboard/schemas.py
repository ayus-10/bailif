import re
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.features.tasks.schemas import TaskRead


class TaskboardCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default="", max_length=5000)
    color: str | None = Field(None, pattern=r"#[0-9a-fA-F]{6}")
    project_id: UUID | None = None


class TaskboardUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=5000)
    color: str | None = Field(None, pattern=r"#[0-9a-fA-F]{6}")


class TaskboardTaskRead(BaseModel):
    id: UUID
    task_id: UUID
    position: int
    task: TaskRead | None = None

    class Config:
        from_attributes = True


class TaskboardRead(BaseModel):
    id: UUID
    name: str
    description: str
    color: str | None
    project_id: UUID | None
    created_at: datetime
    updated_at: datetime
    tasks: List[TaskboardTaskRead] = []

    class Config:
        from_attributes = True


class TaskboardListRead(BaseModel):
    id: UUID
    name: str
    description: str
    color: str | None
    project_id: UUID | None
    task_count: int

    class Config:
        from_attributes = True


class TaskAssignment(BaseModel):
    task_id: UUID
    position: int | None = Field(default=None, ge=0)


class TaskReposition(BaseModel):
    task_id: UUID
    position: int = Field(ge=0)


class TaskboardListResponse(BaseModel):
    items: list[TaskboardListRead]
