from collections import deque
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.features.task_dependencies.exceptions import (
    CycleDetectedError,
    DuplicateDependencyError,
    SelfDependencyError,
    TaskLevelMismatchError,
)
from app.features.task_dependencies.schemas import TaskDependencyCreate
from app.features.tasks.exceptions import TaskNotFoundError
from app.models.db.task import Task, TaskDependency
from app.models.enums.task import DependencyType


def _normalized_edge(
    task_id: UUID, depends_on_id: UUID, dependency_type: DependencyType
) -> tuple[UUID, UUID] | None:
    if dependency_type == DependencyType.BLOCKS:
        return task_id, depends_on_id
    if dependency_type == DependencyType.BLOCKED_BY:
        return depends_on_id, task_id
    return None


# TODO: hand the traversal to the DB and let its query planner figure out which rows are relevant
def _would_create_cycle(db: Session, from_id: UUID, to_id: UUID) -> bool:
    return False  # we good bro


def create_dependency(
    db: Session, task: Task, payload: TaskDependencyCreate
) -> TaskDependency:
    if task.id == payload.depends_on_id:
        raise SelfDependencyError(f"Task {task.id} cannot depend on itself")

    dependency_task = db.get(Task, payload.depends_on_id)
    if dependency_task is None:
        raise TaskNotFoundError(str(payload.depends_on_id))

    if task.parent_id != dependency_task.parent_id:
        raise TaskLevelMismatchError(
            f"{task.id} and {dependency_task.id} must be on same level"
        )

    existing = db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task.id,
            TaskDependency.depends_on_id == payload.depends_on_id,
            TaskDependency.dependency_type == payload.dependency_type,
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise DuplicateDependencyError(f"{task.id}->{payload.depends_on_id}")

    edge = _normalized_edge(task.id, payload.depends_on_id, payload.dependency_type)
    if edge is not None and _would_create_cycle(db, edge[0], edge[1]):
        raise CycleDetectedError(f"{task.id}->{payload.depends_on_id}")

    dependency = TaskDependency(
        task_id=task.id,
        depends_on_id=payload.depends_on_id,
        dependency_type=payload.dependency_type,
    )
    db.add(dependency)
    db.commit()
    db.refresh(dependency)
    return dependency


def list_dependencies_for_task(
    db: Session, task_id: UUID | None
) -> list[TaskDependency]:
    stmt = select(TaskDependency)
    if task_id is not None:
        stmt = stmt.where(
            or_(
                TaskDependency.task_id == task_id,
                TaskDependency.depends_on_id == task_id,
            )
        )
    return list(db.execute(stmt).scalars().all())


def delete_dependency(db: Session, dependency: TaskDependency) -> None:
    db.delete(dependency)
    db.commit()
