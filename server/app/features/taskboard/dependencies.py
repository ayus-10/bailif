from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.taskboard.exceptions import TaskboardNotFoundError
from app.models.db import Project, Taskboard, TaskboardTask, User


def get_taskboard_by_id(
    board_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Taskboard:
    board = db.execute(
        select(Taskboard)
        .join(Project, Taskboard.project_id == Project.id)
        .where(
            Taskboard.id == board_id,
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if board is None:
        raise TaskboardNotFoundError(str(board_id))
    return board
