from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.taskboard.exceptions import (
    TaskboardNotFoundError,
    TaskNotInBoardError,
)
from app.features.taskboard.schemas import TaskAssignment
from app.features.tasks.dependencies import get_owned_task, resolve_owned_task
from app.models.db import Project, Task, Taskboard, User


def get_owned_taskboard(
    taskboard_public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Taskboard:
    board = db.execute(
        select(Taskboard)
        .join(Project, Taskboard.project_id == Project.id)
        .where(
            Taskboard.public_id == taskboard_public_id,
            Taskboard.deleted_at.is_(None),
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if board is None:
        raise TaskboardNotFoundError(
            f"Taskboard with public_id {taskboard_public_id} not found"
        )

    return board


def get_task_on_owned_taskboard(
    taskboard: Taskboard = Depends(get_owned_taskboard),
    task: Task = Depends(get_owned_task),
) -> Task:
    if task.project_id != taskboard.project_id:
        raise TaskNotInBoardError(
            f"Task {task.public_id} is not in board {taskboard.public_id}"
        )
    return task


def get_task_on_owned_taskboard_from_payload(
    payload: TaskAssignment,
    board: Taskboard = Depends(get_owned_taskboard),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Task:
    task = resolve_owned_task(
        task_public_id=payload.task_public_id,
        db=db,
        user=user,
    )

    if task.project_id != board.project_id:
        raise TaskNotInBoardError(
            f"Task {task.public_id} is not in board {board.public_id}"
        )
    return task
