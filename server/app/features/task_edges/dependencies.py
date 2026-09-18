from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.task_edges.exceptions import TaskEdgeNotFoundError
from app.features.task_edges.schemas import TaskEdgeCreate
from app.features.tasks.exceptions import TaskNotFoundError
from app.models.db import Project, Task, User
from app.models.db.task import TaskEdge


def get_task_for_dependencies(
    task_public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Task:
    task = db.execute(
        select(Task)
        .join(Project, Project.id == Task.project_id)
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


def get_depends_on_task_from_payload(
    payload: TaskEdgeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Task:
    task = db.execute(
        select(Task)
        .join(Project, Project.id == Task.project_id)
        .where(
            Task.public_id == payload.depends_on_public_id,
            Task.deleted_at.is_(None),
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if task is None:
        raise TaskNotFoundError(
            f"Task with public_id {payload.depends_on_public_id} not found"
        )

    return task


def get_dependency_on_task(
    dependency_public_id: int,
    task: Task = Depends(get_task_for_dependencies),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskEdge:
    dependency = db.execute(
        select(TaskEdge)
        .join(Task, Task.id == TaskEdge.task_id)
        .join(Project, Project.id == Task.project_id)
        .where(
            TaskEdge.public_id == dependency_public_id,
            Task.deleted_at.is_(None),
            Project.deleted_at.is_(None),
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if dependency is None:
        raise TaskEdgeNotFoundError(f"Task dependency {dependency_public_id} not found")

    is_attached_to_task = (
        dependency.task_id == task.id or dependency.depends_on_id == task.id
    )

    if not is_attached_to_task:
        raise TaskEdgeNotFoundError(f"Task dependency {dependency_public_id} not found")

    return dependency
