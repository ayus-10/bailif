from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db.task import Task
from app.repositories.tasks import services
from app.repositories.tasks.dependencies import get_task_by_id
from app.repositories.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskRead,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    return await services.create_task(db, payload)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    filters: TaskFilterParams = Depends(), db: Session = Depends(get_db)
) -> TaskListResponse:
    return services.list_tasks(db, filters)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task: Task = Depends(get_task_by_id)) -> Task:
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    payload: TaskUpdate,
    task: Task = Depends(get_task_by_id),
    db: Session = Depends(get_db),
) -> Task:
    return await services.update_task(db, task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task: Task = Depends(get_task_by_id), db: Session = Depends(get_db)
) -> None:
    services.delete_task(db, task)
