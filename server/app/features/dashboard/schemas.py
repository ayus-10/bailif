from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.taskboards.schemas import TaskboardListRead
from app.shared.enums import TaskPriority, TaskStatus


class DashboardProjectStats(BaseModel):
    total: int
    active: int


class DashboardTaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int
    by_status: dict[TaskStatus, int]


class DashboardTaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    updated_at: datetime
    project_public_id: int
    project_name: str


class DashboardRead(BaseModel):
    projects: DashboardProjectStats
    tasks: DashboardTaskStats
    upcoming_deadlines: list[DashboardTaskRead]
    recent_activity: list[DashboardTaskRead]
    taskboards: list[TaskboardListRead]
