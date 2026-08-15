from collections import deque
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.db.task import Task, TaskDependency
from app.models.enums.task import DependencyType
from app.repositories.task_dependencies.exceptions import (
    CycleDetectedError,
    DuplicateDependencyError,
    SelfDependencyError,
)
from app.repositories.task_dependencies.schemas import TaskDependencyCreate
from app.repositories.tasks.exceptions import TaskNotFoundError


def _normalized_edge(
    task_id: UUID, depends_on_id: UUID, dependency_type: DependencyType
) -> tuple[UUID, UUID] | None:
    if dependency_type == DependencyType.BLOCKS:
        return task_id, depends_on_id
    if dependency_type == DependencyType.BLOCKED_BY:
        return depends_on_id, task_id
    return None


def _would_create_cycle(db: Session, from_id: UUID, to_id: UUID) -> bool:
    edges = db.execute(
        select(
            TaskDependency.task_id,
            TaskDependency.depends_on_id,
            TaskDependency.dependency_type,
        )
    ).all()

    graph: dict[UUID, list[UUID]] = {}
    for task_id, depends_on_id, dependency_type in edges:
        edge = _normalized_edge(task_id, depends_on_id, dependency_type)
        if edge is None:
            continue
        graph.setdefault(edge[0], []).append(edge[1])

    queue = deque([to_id])
    visited = {to_id}
    while queue:
        current = queue.popleft()
        if current == from_id:
            return True
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False


def create_dependency(
    db: Session, task_id: UUID, payload: TaskDependencyCreate
) -> TaskDependency:
    if task_id == payload.depends_on_id:
        raise SelfDependencyError(f"Task {task_id} cannot depend on itself")

    depends_on_exists = db.get(Task, payload.depends_on_id)
    if depends_on_exists is None:
        raise TaskNotFoundError(str(payload.depends_on_id))

    existing = db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task_id,
            TaskDependency.depends_on_id == payload.depends_on_id,
            TaskDependency.dependency_type == payload.dependency_type,
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise DuplicateDependencyError(f"{task_id}->{payload.depends_on_id}")

    edge = _normalized_edge(task_id, payload.depends_on_id, payload.dependency_type)
    if edge is not None and _would_create_cycle(db, edge[0], edge[1]):
        raise CycleDetectedError(f"{task_id}->{payload.depends_on_id}")

    dependency = TaskDependency(
        task_id=task_id,
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
