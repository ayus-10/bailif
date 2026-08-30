import asyncio
from typing import Tuple
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.exceptions import ValidationError
from app.features.projects.exceptions import ProjectNotFoundError
from app.features.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskRead,
    TaskUpdate,
)
from app.models.db import Project, User
from app.models.db.task import Task
from app.utils.date_validation import validate_task_dates
from app.utils.pagination import decode_cursor, encode_cursor


async def generate_task_embedding(task: Task) -> list[float]:
    embedding_text = f"""
    Title: {task.title}

    Description:
    {task.description}

    Tags:
    {" ".join(task.tags)}

    Status:
    {task.status}

    Priority:
    {task.priority}
    """.strip()

    # return await get_embedding(embedding_text)
    return [0.69 for _ in range(2560)]


def generate_and_save_task_embedding(task_id: UUID):
    db = SessionLocal()
    try:
        task = db.get(Task, task_id)

        if task is None:
            return

        embedding = asyncio.run(generate_task_embedding(task))

        task.embedding = embedding
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_task(
    db: Session,
    payload: TaskCreate,
    user: User,
) -> Task:
    project_exists = db.execute(
        select(Project.id).where(
            Project.id == payload.project_id,
            Project.user_id == user.id,
        )
    ).scalar_one_or_none()

    if project_exists is None:
        raise ProjectNotFoundError(str(payload.project_id))

    task = Task(**payload.model_dump())

    try:
        validate_task_dates(task)
    except ValueError:
        raise ValidationError()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    payload: TaskUpdate,
) -> Tuple[Task, int]:
    updates = payload.model_dump(exclude_unset=True)

    try:
        validate_task_dates(task, updates)
    except ValueError:
        raise ValidationError()

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    updated_field_count = len(updates.items())

    return task, updated_field_count


def list_tasks(db: Session, user: User, filters: TaskFilterParams) -> TaskListResponse:
    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Project.user_id == user.id,
            Task.project_id == filters.project_id,
        )
    )

    if filters.status is not None:
        stmt = stmt.where(Task.status == filters.status)
    if filters.priority is not None:
        stmt = stmt.where(Task.priority == filters.priority)
    if filters.type is not None:
        stmt = stmt.where(Task.type == filters.type)
    if filters.tag is not None:
        stmt = stmt.where(Task.tags.contains(filters.tag))
    if filters.due_before is not None:
        stmt = stmt.where(Task.due_date <= filters.due_before)
    if filters.due_after is not None:
        stmt = stmt.where(Task.due_date >= filters.due_after)

    if filters.only_root:
        stmt = stmt.where(Task.parent_id.is_(None))
    elif filters.parent_id is not None:
        stmt = stmt.where(Task.parent_id == filters.parent_id)

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


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
