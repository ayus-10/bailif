from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db.task import Task, TaskDependency
from app.repositories.task_dependencies import services
from app.repositories.task_dependencies.dependencies import get_task_dependency_by_id
from app.repositories.task_dependencies.schemas import (
    TaskDependencyCreate,
    TaskDependencyRead,
)
from app.repositories.tasks.dependencies import get_task_by_id

router = APIRouter(
    prefix="/tasks/{task_id}/dependencies",
    tags=["task-dependencies"],
)


@router.post(
    "",
    response_model=TaskDependencyRead,
    status_code=status.HTTP_201_CREATED,
)
def create_dependency(
    payload: TaskDependencyCreate,
    task: Task = Depends(get_task_by_id),
    db: Session = Depends(get_db),
) -> TaskDependency:
    return services.create_dependency(db, task.id, payload)


@router.get(
    "",
    response_model=list[TaskDependencyRead],
)
def list_dependencies(
    task: Task = Depends(get_task_by_id),
    db: Session = Depends(get_db),
) -> list[TaskDependency]:
    return services.list_dependencies_for_task(db, task.id)


@router.get(
    "/{dependency_id}",
    response_model=TaskDependencyRead,
)
def get_dependency(
    dependency: TaskDependency = Depends(get_task_dependency_by_id),
) -> TaskDependency:
    return dependency


@router.delete(
    "/{dependency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_dependency(
    dependency: TaskDependency = Depends(get_task_dependency_by_id),
    db: Session = Depends(get_db),
) -> None:
    services.delete_dependency(db, dependency)
