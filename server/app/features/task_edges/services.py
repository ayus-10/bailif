from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.features.task_edges.exceptions import (
    CycleDetectedError,
    DuplicateEdgeError,
    SelfEdgeError,
    TaskLevelMismatchError,
)
from app.features.task_edges.schemas import TaskEdgeCreate
from app.models.db import Task, TaskEdge
from app.models.enums.task import EdgeType


def create_edge(
    db: Session,
    task: Task,
    depends_on_task: Task,
    payload: TaskEdgeCreate,
) -> TaskEdge:
    if task.id == depends_on_task.id:
        raise SelfEdgeError(f"Task {task.public_id} cannot depend on itself")

    if task.parent_id != depends_on_task.parent_id:
        raise TaskLevelMismatchError(
            f"Tasks {task.public_id} and "
            f"{depends_on_task.public_id} must be on the same level"
        )

    existing = db.execute(
        select(TaskEdge).where(
            TaskEdge.task_id == task.id,
            TaskEdge.depends_on_id == depends_on_task.id,
            TaskEdge.edge_type == payload.edge_type,
        )
    ).scalar_one_or_none()

    if existing is not None:
        raise DuplicateEdgeError(
            f"Edge already exists between "
            f"{task.public_id} and {depends_on_task.public_id}"
        )

    edge = _normalized_edge(task.id, depends_on_task.id, payload.edge_type)

    if edge is not None and _would_create_cycle(db, edge[0], edge[1]):
        raise CycleDetectedError(
            f"Adding edge from task {task.public_id} "
            f"to {depends_on_task.public_id} would create a cycle"
        )

    task_edge = TaskEdge(
        task_id=task.id,
        depends_on_id=depends_on_task.id,
        edge_type=payload.edge_type,
    )

    # Assigned directly from objects already in hand rather than re-query
    task_edge.task = task
    task_edge.depends_on = depends_on_task

    db.add(task_edge)
    db.flush()

    # Scoped refresh: bare refresh would expire the two relationship assignments above
    db.refresh(task_edge, attribute_names=["public_id"])

    return task_edge


def list_edges_for_task(db: Session, task: Task) -> list[TaskEdge]:
    stmt = (
        select(TaskEdge)
        .options(
            joinedload(TaskEdge.task),
            joinedload(TaskEdge.depends_on),
        )
        .where(
            or_(
                TaskEdge.task_id == task.id,
                TaskEdge.depends_on_id == task.id,
            )
        )
    )
    return list(db.execute(stmt).scalars().all())


def delete_edge(db: Session, edge: TaskEdge) -> None:
    db.delete(edge)


def _normalized_edge(
    task_id: UUID, depends_on_id: UUID, edge_type: EdgeType
) -> tuple[UUID, UUID] | None:
    if edge_type == EdgeType.BLOCKS:
        return task_id, depends_on_id
    if edge_type == EdgeType.BLOCKED_BY:
        return depends_on_id, task_id
    return None


# TODO: hand the traversal to the DB and let its query planner figure out which rows are relevant
def _would_create_cycle(db: Session, from_id: UUID, to_id: UUID) -> bool:
    return False
