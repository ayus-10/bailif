from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.features.projects.exceptions import ProjectNotFoundError
from app.features.taskboard.exceptions import (
    InvalidTaskPositionError,
    TaskAlreadyInBoardError,
    TaskNotInBoardError,
)
from app.features.taskboard.schemas import (
    TaskboardCreate,
    TaskboardListRead,
    TaskboardListResponse,
    TaskboardUpdate,
)
from app.features.tasks.exceptions import TaskNotFoundError
from app.models.db.project import Project
from app.models.db.task import Task
from app.models.db.taskboard import Taskboard, TaskboardTask


def create_taskboard(
    db: Session,
    payload: TaskboardCreate,
) -> Taskboard:
    if payload.project_id is not None:
        project = db.get(Project, payload.project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {payload.project_id} not found")

    board = Taskboard(**payload.model_dump())

    db.add(board)
    db.commit()
    db.refresh(board)

    return board


def update_taskboard(
    db: Session,
    board: Taskboard,
    payload: TaskboardUpdate,
) -> Taskboard:
    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(board, field, value)

    db.commit()
    db.refresh(board)

    return board


def list_taskboards(
    db: Session,
    project_id: UUID | None = None,
) -> TaskboardListResponse:
    stmt = (
        select(
            Taskboard,
            func.count(Task.id).label("task_count"),
        )
        .outerjoin(
            TaskboardTask,
            TaskboardTask.taskboard_id == Taskboard.id,
        )
        .outerjoin(
            Task,
            Task.id == TaskboardTask.task_id,
        )
    )

    if project_id is not None:
        stmt = stmt.where(Taskboard.project_id == project_id)

    stmt = stmt.group_by(Taskboard.id).order_by(
        Taskboard.created_at.asc(),
        Taskboard.id.asc(),
    )

    rows = db.execute(stmt).all()

    return TaskboardListResponse(
        items=[
            TaskboardListRead(
                id=taskboard.id,
                name=taskboard.name,
                description=taskboard.description,
                color=taskboard.color,
                project_id=taskboard.project_id,
                task_count=task_count,
            )
            for taskboard, task_count in rows
        ],
    )


def delete_taskboard(
    db: Session,
    board: Taskboard,
) -> None:
    db.delete(board)
    db.commit()


def add_task_to_board(
    db: Session,
    board: Taskboard,
    task_id: UUID,
    position: int | None = None,
) -> TaskboardTask:
    task = db.get(Task, task_id)

    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")

    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task_id,
    )
    existing = db.execute(stmt).scalar_one_or_none()

    if existing is not None:
        raise TaskAlreadyInBoardError()

    count_stmt = (
        select(func.count())
        .select_from(TaskboardTask)
        .where(
            TaskboardTask.taskboard_id == board.id,
        )
    )
    task_count = db.execute(count_stmt).scalar_one()

    if position is None or position > task_count:
        position = task_count

    stmt = (
        update(TaskboardTask)
        .where(
            TaskboardTask.taskboard_id == board.id,
            TaskboardTask.position >= position,
        )
        .values(position=TaskboardTask.position + 1)
    )
    db.execute(stmt)

    association = TaskboardTask(
        taskboard_id=board.id,
        task_id=task.id,
        position=position,
    )

    db.add(association)
    db.commit()
    db.refresh(association)

    return association


def remove_task_from_board(
    db: Session,
    board: Taskboard,
    task_id: UUID,
) -> None:
    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task_id,
    )
    association = db.execute(stmt).scalar_one_or_none()

    if association is None:
        raise TaskNotInBoardError()

    position = association.position

    db.delete(association)

    stmt = (
        update(TaskboardTask)
        .where(
            TaskboardTask.taskboard_id == board.id,
            TaskboardTask.position > position,
        )
        .values(position=TaskboardTask.position - 1)
    )
    db.execute(stmt)

    db.commit()


def reposition_task_in_board(
    db: Session,
    board: Taskboard,
    task_id: UUID,
    position: int,
) -> None:
    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task_id,
    )
    association = db.execute(stmt).scalar_one_or_none()

    if association is None:
        raise TaskNotInBoardError()

    old_position = association.position

    if old_position == position:
        return

    count_stmt = (
        select(func.count())
        .select_from(TaskboardTask)
        .where(
            TaskboardTask.taskboard_id == board.id,
        )
    )
    task_count = db.execute(count_stmt).scalar_one()

    if position >= task_count:
        raise InvalidTaskPositionError()

    if position > old_position:
        stmt = (
            update(TaskboardTask)
            .where(
                TaskboardTask.taskboard_id == board.id,
                TaskboardTask.position > old_position,
                TaskboardTask.position <= position,
            )
            .values(position=TaskboardTask.position - 1)
        )
        db.execute(stmt)
    else:
        stmt = (
            update(TaskboardTask)
            .where(
                TaskboardTask.taskboard_id == board.id,
                TaskboardTask.position >= position,
                TaskboardTask.position < old_position,
            )
            .values(position=TaskboardTask.position + 1)
        )
        db.execute(stmt)

    association.position = position

    db.commit()
