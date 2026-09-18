from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.features.task_dependencies.exceptions import (
    CycleDetectedError,
    DuplicateDependencyError,
    SelfDependencyError,
    TaskLevelMismatchError,
)
from app.features.task_dependencies.schemas import TaskDependencyCreate
from app.models.db.task import Task, TaskDependency
from app.models.enums.task import DependencyType


def create_dependency(
    db: Session,
    task: Task,
    depends_on_task: Task,
    payload: TaskDependencyCreate,
) -> TaskDependency:
    if task.id == depends_on_task.id:
        raise SelfDependencyError(f"Task {task.public_id} cannot depend on itself")

    if task.parent_id != depends_on_task.parent_id:
        raise TaskLevelMismatchError(
            f"Tasks {task.public_id} and "
            f"{depends_on_task.public_id} must be on the same level"
        )

    existing = db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task.id,
            TaskDependency.depends_on_id == depends_on_task.id,
            TaskDependency.dependency_type == payload.dependency_type,
        )
    ).scalar_one_or_none()

    if existing is not None:
        raise DuplicateDependencyError(
            f"Dependency already exists between "
            f"{task.public_id} and {depends_on_task.public_id}"
        )

    edge = _normalized_edge(task.id, depends_on_task.id, payload.dependency_type)

    if edge is not None and _would_create_cycle(db, edge[0], edge[1]):
        raise CycleDetectedError(
            f"Adding dependency from task {task.public_id} "
            f"to {depends_on_task.public_id} would create a cycle"
        )

    dependency = TaskDependency(
        task_id=task.id,
        depends_on_id=depends_on_task.id,
        dependency_type=payload.dependency_type,
    )

    # Assigned directly from objects already in hand rather than re-query
    dependency.task = task
    dependency.depends_on = depends_on_task

    db.add(dependency)
    db.flush()

    # Scoped refresh: bare refresh would expire the two relationship assignments above
    db.refresh(dependency, attribute_names=["public_id"])

    return dependency


def list_dependencies_for_task(db: Session, task: Task) -> list[TaskDependency]:
    stmt = (
        select(TaskDependency)
        .options(
            joinedload(TaskDependency.task),
            joinedload(TaskDependency.depends_on),
        )
        .where(
            or_(
                TaskDependency.task_id == task.id,
                TaskDependency.depends_on_id == task.id,
            )
        )
    )
    return list(db.execute(stmt).scalars().all())


def delete_dependency(db: Session, dependency: TaskDependency) -> None:
    db.delete(dependency)


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
    return False
