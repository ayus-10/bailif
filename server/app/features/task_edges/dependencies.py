from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.features.task_edges.exceptions import TaskEdgeNotFoundError
from app.features.task_edges.schemas import TaskEdgeCreate
from app.features.tasks.dependencies import resolve_owned_task
from app.features.tasks.exceptions import TaskNotFoundError
from app.models.db import Project, Task, User
from app.models.db.task import TaskEdge


def get_task_for_edges(
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
    return resolve_owned_task(
        task_public_id=payload.depends_on_public_id,
        db=db,
        user=user,
    )


def get_edge_on_task(
    edge_public_id: int,
    task: Task = Depends(get_task_for_edges),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TaskEdge:
    edge = db.execute(
        select(TaskEdge)
        .join(Task, Task.id == TaskEdge.task_id)
        .join(Project, Project.id == Task.project_id)
        .where(
            TaskEdge.public_id == edge_public_id,
            Task.deleted_at.is_(None),
            Project.deleted_at.is_(None),
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if edge is None:
        raise TaskEdgeNotFoundError(f"Task edge {edge_public_id} not found")

    is_attached_to_task = edge.task_id == task.id or edge.depends_on_id == task.id

    if not is_attached_to_task:
        raise TaskEdgeNotFoundError(f"Task edge {edge_public_id} not found")

    return edge
