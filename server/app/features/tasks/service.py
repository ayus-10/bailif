from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.tasks.schemas import TaskCreate, TaskFilterParams, TaskUpdate
from app.models.db.task import Task


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, filters: TaskFilterParams) -> list[Task]:
    stmt = select(Task)

    if filters.project_id is not None:
        stmt = stmt.where(Task.project_id == filters.project_id)
    if filters.status is not None:
        stmt = stmt.where(Task.status == filters.status.value)
    if filters.priority is not None:
        stmt = stmt.where(Task.priority == filters.priority.value)
    if filters.type is not None:
        stmt = stmt.where(Task.type == filters.type.value)
    if filters.parent_id is not None:
        stmt = stmt.where(Task.parent_id == filters.parent_id)

    stmt = stmt.limit(filters.limit).offset(filters.offset)
    return list(db.execute(stmt).scalars().all())


def update_task(db: Session, task: Task, payload: TaskUpdate) -> Task:
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
