from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db.task import TaskDependency
from app.repositories.task_dependencies.exceptions import TaskDependencyNotFoundError


def get_task_dependency_by_id(
    task_id: UUID,
    dependency_id: UUID,
    db: Session = Depends(get_db),
) -> TaskDependency:
    dependency = (
        db.query(TaskDependency)
        .filter(
            TaskDependency.id == dependency_id,
            TaskDependency.task_id == task_id,
        )
        .first()
    )

    if dependency is None:
        raise TaskDependencyNotFoundError(str(dependency_id))
    return dependency
