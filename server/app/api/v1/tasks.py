from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.tasks import services
from app.features.tasks.dependencies import get_task_by_id
from app.features.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskRead,
    TaskUpdate,
)
from app.models.db.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Task:
    return services.create_task(db, payload, background_tasks)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    filters: TaskFilterParams = Depends(), db: Session = Depends(get_db)
) -> TaskListResponse:
    return services.list_tasks(db, filters)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task: Task = Depends(get_task_by_id)) -> Task:
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    payload: TaskUpdate,
    background_tasks: BackgroundTasks,
    task: Task = Depends(get_task_by_id),
    db: Session = Depends(get_db),
) -> Task:
    return services.update_task(db, task, payload, background_tasks)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task: Task = Depends(get_task_by_id), db: Session = Depends(get_db)
) -> None:
    services.delete_task(db, task)
