from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.agent.llm.embeddings import get_embedding
from app.core.pagination import decode_cursor, encode_cursor
from app.features.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskRead,
    TaskUpdate,
)
from app.models.db.task import Task


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    # TODO: make use of bg workers for this
    task.embedding = get_embedding(f"{task.title}\n{task.description}")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, filters: TaskFilterParams) -> TaskListResponse:
    stmt = select(Task)

    if filters.project_id is not None:
        stmt = stmt.where(Task.project_id == filters.project_id)
    if filters.status is not None:
        stmt = stmt.where(Task.status == filters.status)
    if filters.priority is not None:
        stmt = stmt.where(Task.priority == filters.priority)
    if filters.type is not None:
        stmt = stmt.where(Task.type == filters.type)
    if filters.tag is not None:
        stmt = stmt.where(Task.tags.contains(filters.tag))
    if filters.parent_id is not None:
        stmt = stmt.where(Task.parent_id == filters.parent_id)
    if filters.due_before is not None:
        stmt = stmt.where(Task.due_date <= filters.due_before)
    if filters.due_after is not None:
        stmt = stmt.where(Task.due_date >= filters.due_after)

    if filters.cursor is not None:
        cursor_created_at, cursor_id = decode_cursor(filters.cursor)
        stmt = stmt.where(
            or_(
                Task.created_at < cursor_created_at,
                and_(Task.created_at == cursor_created_at, Task.id < cursor_id),
            )
        )

    stmt = stmt.order_by(Task.created_at.desc(), Task.id.desc())
    stmt = stmt.limit(filters.limit + 1)

    rows = list(db.execute(stmt).scalars().all())

    next_cursor = None
    if len(rows) > filters.limit:
        rows = rows[: filters.limit]
        last = rows[-1]
        next_cursor = encode_cursor(last.created_at, last.id)

    return TaskListResponse(
        items=[TaskRead.model_validate(row) for row in rows],
        next_cursor=next_cursor,
    )


def update_task(db: Session, task: Task, payload: TaskUpdate) -> Task:
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    # TODO: make use of bg workers for this
    if "title" in updates or "description" in updates:
        task.embedding = get_embedding(f"{task.title}\n{task.description}")

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
