from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.features.tasks.schemas import TaskRead


class TaskboardCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=50000)
    color: str | None = Field(None, pattern=r"#[0-9a-fA-F]{6}")


class TaskboardUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=50000)
    color: str | None = Field(None, pattern=r"#[0-9a-fA-F]{6}")


class TaskboardTaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    position: int
    task: TaskRead | None = None


class TaskboardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: int
    name: str
    description: str
    color: str | None
    project_public_id: int
    created_at: datetime
    updated_at: datetime
    tasks: list[TaskboardTaskRead] = Field(default_factory=list)


class TaskboardListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: int
    name: str
    description: str
    color: str | None
    project_public_id: int
    task_count: int


class TaskAssignment(BaseModel):
    task_public_id: int
    position: int | None = Field(default=None, ge=0)


class TaskReposition(BaseModel):
    position: int = Field(ge=0)


class TaskboardListResponse(BaseModel):
    items: list[TaskboardListRead]
