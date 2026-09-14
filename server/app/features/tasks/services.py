import asyncio
from typing import Tuple
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.agent.llm.embeddings import get_embedding
from app.core.database import SessionLocal
from app.core.exceptions import ValidationError
from app.features.projects.exceptions import ProjectNotFoundError
from app.features.tasks.schemas import (
    TaskCreate,
    TaskFilterParams,
    TaskListResponse,
    TaskUpdate,
)
from app.models.db import Project, Taskboard, TaskboardTask, User
from app.models.db.task import Task
from app.utils.date_validation import validate_datetime_range
from app.utils.model_to_read import task_to_read
from app.utils.pagination import decode_cursor, encode_cursor


def create_task(
    db: Session,
    payload: TaskCreate,
    user: User,
) -> Task:
    if user.active_project is None:
        raise ProjectNotFoundError("User must have an active project")

    project = db.execute(
        select(Project).where(
            Project.public_id == user.active_project.public_id,
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(
            f"Active project {user.active_project.public_id} not found"
        )

    parent_id = (
        select(Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.public_id == payload.parent_public_id,
            Task.deleted_at.is_(None),
            Project.user_id == user.id,
        )
        .scalar_subquery()
        if payload.parent_public_id is not None
        else None
    )

    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        type=payload.type,
        tags=payload.tags,
        start_date=payload.start_date,
        due_date=payload.due_date,
        project_id=project.id,
        parent_id=parent_id,
    )

    try:
        _validate_task_dates(task)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    db.add(task)
    db.flush()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    payload: TaskUpdate,
) -> Tuple[Task, int]:
    updates = {}

    if "title" in payload.model_fields_set:
        updates["title"] = payload.title
    if "description" in payload.model_fields_set:
        updates["description"] = payload.description
    if "status" in payload.model_fields_set:
        updates["status"] = payload.status
    if "priority" in payload.model_fields_set:
        updates["priority"] = payload.priority
    if "type" in payload.model_fields_set:
        updates["type"] = payload.type
    if "tags" in payload.model_fields_set:
        updates["tags"] = payload.tags
    if "start_date" in payload.model_fields_set:
        updates["start_date"] = payload.start_date
    if "due_date" in payload.model_fields_set:
        updates["due_date"] = payload.due_date
    if "parent_public_id" in payload.model_fields_set:
        if payload.parent_public_id is None:
            updates["parent_id"] = None
        else:
            updates["parent_id"] = (
                select(Task.id)
                .join(Project, Task.project_id == Project.id)
                .where(
                    Task.public_id == payload.parent_public_id,
                    Task.deleted_at.is_(None),
                    Project.user_id == task.project.user_id,
                )
                .scalar_subquery()
            )

    try:
        _validate_task_dates(task, updates)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    for field, value in updates.items():
        setattr(task, field, value)

    db.flush()
    db.refresh(task)

    updated_field_count = len(updates)

    return task, updated_field_count


def list_tasks(
    db: Session,
    user: User,
    filters: TaskFilterParams,
) -> TaskListResponse:
    if user.active_project is None:
        raise ProjectNotFoundError("User must have an active project")

    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Project.user_id == user.id,
            Task.project_id == user.active_project.id,
            Task.deleted_at.is_(None),
        )
    )

    if filters.taskboard_public_id is not None:
        stmt = (
            stmt.join(
                TaskboardTask,
                TaskboardTask.task_id == Task.id,
            )
            .join(
                Taskboard,
                Taskboard.id == TaskboardTask.taskboard_id,
            )
            .where(
                Taskboard.public_id == filters.taskboard_public_id,
                Taskboard.deleted_at.is_(None),
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
    elif filters.parent_public_id is not None:
        parent_id = (
            select(Task.id)
            .join(Project, Task.project_id == Project.id)
            .where(
                Task.public_id == filters.parent_public_id,
                Task.deleted_at.is_(None),
                Project.user_id == user.id,
            )
            .scalar_subquery()
        )
        stmt = stmt.where(Task.parent_id == parent_id)

    if filters.cursor is not None:
        cursor_created_at, cursor_public_id = decode_cursor(filters.cursor)
        stmt = stmt.where(
            or_(
                Task.created_at < cursor_created_at,
                and_(
                    Task.created_at == cursor_created_at,
                    Task.public_id < cursor_public_id,
                ),
            )
        )

    stmt = stmt.order_by(Task.created_at.desc(), Task.public_id.desc())
    stmt = stmt.limit(filters.limit + 1)

    rows = list(db.execute(stmt).scalars().all())

    next_cursor = None
    if len(rows) > filters.limit:
        rows = rows[: filters.limit]
        last = rows[-1]
        next_cursor = encode_cursor(
            last.created_at,
            last.public_id,
        )

    return TaskListResponse(
        items=[task_to_read(row) for row in rows],
        next_cursor=next_cursor,
    )


def delete_task(db: Session, task: Task, user: User) -> None:
    task.soft_delete(deleted_by=user.id)
    db.flush()


def generate_and_save_task_embedding(task_id: UUID):
    db = SessionLocal()
    try:
        task = db.get(Task, task_id)

        if task is None:
            return

        embedding = asyncio.run(_generate_task_embedding(task))

        task.embedding = embedding
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _validate_task_dates(task: "Task", updates: dict = {}) -> None:
    start = updates.get("start_date", task.start_date)
    due = updates.get("due_date", task.due_date)
    validate_datetime_range(start, due)


async def _generate_task_embedding(task: Task) -> list[float]:
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

    return await get_embedding(embedding_text)
