from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.task_dependencies import services
from app.features.task_dependencies.dependencies import (
    get_dependency_on_task,
    get_depends_on_task_from_payload,
    get_task_for_dependencies,
)
from app.features.task_dependencies.schemas import (
    TaskDependencyCreate,
    TaskDependencyRead,
)
from app.models.db import Task, TaskDependency
from app.utils.model_to_read import task_dependency_to_read

router = APIRouter(
    prefix="/tasks/{task_public_id}/dependencies",
    tags=["task-dependencies"],
)


@router.post(
    "",
    response_model=TaskDependencyRead,
    status_code=status.HTTP_201_CREATED,
)
def create_dependency(
    payload: TaskDependencyCreate,
    task: Task = Depends(get_task_for_dependencies),
    depends_on_task: Task = Depends(get_depends_on_task_from_payload),
    db: Session = Depends(get_db),
) -> TaskDependencyRead:
    dependency = services.create_dependency(db, task, depends_on_task, payload)
    return task_dependency_to_read(dependency)


@router.get(
    "",
    response_model=list[TaskDependencyRead],
)
def list_dependencies(
    task: Task = Depends(get_task_for_dependencies),
    db: Session = Depends(get_db),
) -> list[TaskDependencyRead]:
    dependencies = services.list_dependencies_for_task(db, task)
    live = [
        d
        for d in dependencies
        if d.task.deleted_at is None and d.depends_on.deleted_at is None
    ]
    return [task_dependency_to_read(d) for d in live]


@router.delete(
    "/{dependency_public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_dependency(
    dependency: TaskDependency = Depends(get_dependency_on_task),
    db: Session = Depends(get_db),
) -> None:
    services.delete_dependency(db, dependency)
