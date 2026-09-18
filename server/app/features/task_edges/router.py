from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.task_edges import services
from app.features.task_edges.dependencies import (
    get_depends_on_task_from_payload,
    get_edge_on_task,
    get_task_for_edges,
)
from app.features.task_edges.schemas import (
    TaskEdgeCreate,
    TaskEdgeRead,
)
from app.models.db import Task, TaskEdge
from app.utils.model_to_read import task_edge_to_read

router = APIRouter(
    prefix="/tasks/{task_public_id}/edges",
    tags=["task-edges"],
)


@router.post(
    "",
    response_model=TaskEdgeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_edge(
    payload: TaskEdgeCreate,
    task: Task = Depends(get_task_for_edges),
    depends_on_task: Task = Depends(get_depends_on_task_from_payload),
    db: Session = Depends(get_db),
) -> TaskEdgeRead:
    edge = services.create_edge(db, task, depends_on_task, payload)
    return task_edge_to_read(edge)


@router.get(
    "",
    response_model=list[TaskEdgeRead],
)
def list_edges(
    task: Task = Depends(get_task_for_edges),
    db: Session = Depends(get_db),
) -> list[TaskEdgeRead]:
    edges = services.list_edges_for_task(db, task)
    live = [
        d
        for d in edges
        if d.task.deleted_at is None and d.depends_on.deleted_at is None
    ]
    return [task_edge_to_read(d) for d in live]


@router.delete(
    "/{edge_public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_edge(
    edge: TaskEdge = Depends(get_edge_on_task),
    db: Session = Depends(get_db),
) -> None:
    services.delete_edge(db, edge)
