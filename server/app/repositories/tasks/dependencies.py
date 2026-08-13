from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db.task import Task
from app.repositories.tasks.exceptions import TaskNotFoundError


def get_task_by_id(task_id: UUID, db: Session = Depends(get_db)) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError(str(task_id))
    return task
