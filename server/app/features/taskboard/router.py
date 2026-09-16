from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.projects.dependencies import get_project_by_public_id
from app.features.taskboard import services
from app.features.taskboard.dependencies import get_taskboard_by_public_id
from app.features.taskboard.schemas import (
    TaskAssignment,
    TaskboardCreate,
    TaskboardListResponse,
    TaskboardRead,
    TaskboardTaskRead,
    TaskboardUpdate,
    TaskReposition,
)
from app.features.tasks.dependencies import get_task_by_public_id
from app.models.db import Project, Task, User
from app.models.db.taskboard import Taskboard, TaskboardTask

router = APIRouter(prefix="/taskboards", tags=["taskboards"])


@router.post(
    "",
    response_model=TaskboardRead,
    status_code=status.HTTP_201_CREATED,
)
def create_taskboard(
    payload: TaskboardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskboardRead:
    board = services.create_taskboard(db, user, payload)
    return taskboard_to_read(board)  # this utility funco dont exist


@router.get(
    "",
    response_model=TaskboardListResponse,
)
def list_taskboards(
    project: Project = Depends(get_project_by_public_id),
    db: Session = Depends(get_db),
) -> TaskboardListResponse:
    return services.list_taskboards(db, project)


@router.get(
    "/{public_id}",
    response_model=TaskboardRead,
)
def get_taskboard(
    board: Taskboard = Depends(get_taskboard_by_public_id),
) -> TaskboardRead:
    return taskboard_to_read(board)  # this utility funco dont exist


@router.patch(
    "/{public_id}",
    response_model=TaskboardRead,
)
def update_taskboard(
    payload: TaskboardUpdate,
    board: Taskboard = Depends(get_taskboard_by_public_id),
    db: Session = Depends(get_db),
) -> TaskboardRead:
    board = services.update_taskboard(db, board, payload)
    return taskboard_to_read(board)  # this utility funco dont exist


@router.delete(
    "/{public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_taskboard(
    board: Taskboard = Depends(get_taskboard_by_public_id),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    services.delete_taskboard(db, board, user)


@router.post(
    "/{public_id}/tasks",
    response_model=TaskboardTaskRead,
    status_code=status.HTTP_201_CREATED,
)
def add_task_to_board(
    payload: TaskAssignment,
    board: Taskboard = Depends(get_taskboard_by_public_id), # not sure if this is gonna resolve from the url above
    task: Task = Depends(get_task_by_public_id), # not sure if this is gonna resolve from the url above
    db: Session = Depends(get_db),
) -> TaskboardTask:  # do not return db model
    return services.add_task_to_board(
        db=db,
        board=board,
        task=task,
        position=payload.position,
    )


@router.delete(
    "/{public_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task_from_board(
    task: Task = Depends(get_task_by_public_id), # not sure if this is gonna resolve from the url above
    board: Taskboard = Depends(get_taskboard_by_public_id), # not sure if this is gonna resolve from the url above
    db: Session = Depends(get_db),
) -> None:
    services.remove_task_from_board(
        db=db,
        board=board,
        task=task,
    )


@router.patch(
    "/{public_id}/tasks/reposition",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reposition_task(
    payload: TaskReposition,
    task: Task = Depends(get_task_by_public_id), # not sure if this is gonna resolve from the url above
    board: Taskboard = Depends(get_taskboard_by_public_id), # not sure if this is gonna resolve from the url above
    db: Session = Depends(get_db),
) -> None:
    services.reposition_task_in_board(
        db=db,
        board=board,
        task=task,
        position=payload.position,
    )
