from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.tasks import get_owned_task
from app.features.tasks import services
from app.features.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskRead,
    TaskUpdate,
)
from app.models.db import User
from app.models.db.task import Task
from app.utils.model_to_read import task_to_read

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskRead:
    task = services.create_task(db, payload, user)

    background_tasks.add_task(
        services.generate_and_save_task_embedding,
        task.id,
    )

    return task_to_read(task)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    filters: TaskFilterParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskListResponse:
    return services.list_tasks(db, user, filters)


@router.get("/{task_public_id}", response_model=TaskRead)
def get_task(
    task: Task = Depends(get_owned_task),
) -> TaskRead:
    return task_to_read(task)


@router.patch("/{task_public_id}", response_model=TaskRead)
def update_task(
    payload: TaskUpdate,
    background_tasks: BackgroundTasks,
    task: Task = Depends(get_owned_task),
    db: Session = Depends(get_db),
) -> TaskRead:
    task, updated_field_count = services.update_task(
        db,
        task,
        payload,
    )

    if updated_field_count > 0:
        background_tasks.add_task(
            services.generate_and_save_task_embedding,
            task.id,
        )

    return task_to_read(task)


@router.delete(
    "/{task_public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task: Task = Depends(get_owned_task),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    services.delete_task(db, task, user)
