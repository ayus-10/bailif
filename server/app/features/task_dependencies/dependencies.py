from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.task_dependencies.exceptions import TaskDependencyNotFoundError
from app.models.db import Project, Task, User
from app.models.db.task import TaskDependency


def get_task_dependency_by_id(
    task_public_id: int,
    dependency_public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskDependency:
    dependency = db.execute(
        select(TaskDependency)
        .join(Task, Task.id == TaskDependency.task_id)
        .join(Project, Project.id == Task.project_id)
        .where(
            TaskDependency.public_id == dependency_public_id,
            Task.public_id == task_public_id,
            Task.deleted_at.is_(None),
            Project.deleted_at.is_(None),
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if dependency is None:
        raise TaskDependencyNotFoundError(
            f"Task dependency {dependency_public_id} not found"
        )

    return dependency
