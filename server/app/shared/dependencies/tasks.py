from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db import Project, Task, User
from app.shared.dependencies.auth import get_current_user
from app.shared.exceptions import TaskNotFoundError


def get_owned_task(
    task_public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Task:
    task = db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.public_id == task_public_id,
            Task.deleted_at.is_(None),
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if task is None:
        raise TaskNotFoundError(f"Task with public_id {task_public_id} not found")

    return task
