from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.projects.dependencies import get_project_by_id
from app.features.taskboard import services
from app.features.taskboard.dependencies import get_taskboard_by_id
from app.features.taskboard.schemas import (
    TaskAssignment,
    TaskboardCreate,
    TaskboardListResponse,
    TaskboardRead,
    TaskboardTaskRead,
    TaskboardUpdate,
    TaskReposition,
)
from app.models.db import Project, User
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
) -> Taskboard:
    return services.create_taskboard(db, user, payload)


@router.get(
    "",
    response_model=TaskboardListResponse,
)
def list_taskboards(
    project: Project = Depends(get_project_by_id),
    db: Session = Depends(get_db),
) -> TaskboardListResponse:
    return services.list_taskboards(db, project.id)


@router.get(
    "/{board_id}",
    response_model=TaskboardRead,
)
def get_taskboard(
    board: Taskboard = Depends(get_taskboard_by_id),
) -> Taskboard:
    return board


@router.patch(
    "/{board_id}",
    response_model=TaskboardRead,
)
def update_taskboard(
    payload: TaskboardUpdate,
    board: Taskboard = Depends(get_taskboard_by_id),
    db: Session = Depends(get_db),
) -> Taskboard:
    return services.update_taskboard(db, board, payload)


@router.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_taskboard(
    board: Taskboard = Depends(get_taskboard_by_id),
    db: Session = Depends(get_db),
) -> None:
    services.delete_taskboard(db, board)


@router.post(
    "/{board_id}/tasks",
    response_model=TaskboardTaskRead,
    status_code=status.HTTP_201_CREATED,
)
def add_task_to_board(
    payload: TaskAssignment,
    board: Taskboard = Depends(get_taskboard_by_id),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskboardTask:
    return services.add_task_to_board(
        db=db,
        board=board,
        user=user,
        task_id=payload.task_id,
        position=payload.position,
    )


@router.delete(
    "/{board_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task_from_board(
    task_id: UUID,
    board: Taskboard = Depends(get_taskboard_by_id),
    db: Session = Depends(get_db),
) -> None:
    services.remove_task_from_board(
        db=db,
        board=board,
        task_id=task_id,
    )


@router.patch(
    "/{board_id}/tasks/reposition",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reposition_task(
    payload: TaskReposition,
    board: Taskboard = Depends(get_taskboard_by_id),
    db: Session = Depends(get_db),
) -> None:
    services.reposition_task_in_board(
        db=db,
        board=board,
        task_id=payload.task_id,
        position=payload.position,
    )
