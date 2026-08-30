from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.task_dependencies.exceptions import TaskDependencyNotFoundError
from app.models.db import Project, Task, User
from app.models.db.task import TaskDependency


def get_task_dependency_by_id(
    task_id: UUID,
    dependency_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskDependency:
    dependency = db.execute(
        select(TaskDependency)
        .join(Task, Task.id == TaskDependency.task_id)
        .join(Project, Project.id == Task.project_id)
        .where(
            TaskDependency.id == dependency_id,
            Task.id == task_id,
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if dependency is None:
        raise TaskDependencyNotFoundError(str(dependency_id))
    return dependency
