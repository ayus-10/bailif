from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.tasks.exceptions import TaskNotFoundError
from app.models.db import Project, User
from app.models.db.task import Task


def get_task_by_id(
    task_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Task:
    task = db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.id == task_id,
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if task is None:
        raise TaskNotFoundError(str(task_id))

    return task
