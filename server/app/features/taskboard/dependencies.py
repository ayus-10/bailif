from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.taskboard.exceptions import TaskboardNotFoundError
from app.models.db import Project, Taskboard, User


def get_taskboard_by_public_id(
    public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Taskboard:
    board = db.execute(
        select(Taskboard)
        .join(Project, Taskboard.project_id == Project.id)
        .where(
            Taskboard.public_id == public_id,
            Taskboard.deleted_at.is_(None),
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if board is None:
        raise TaskboardNotFoundError(f"Taskboard with public_id {public_id} not found")

    return board
