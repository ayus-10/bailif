from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, raiseload

from app.features.taskboards.exceptions import (
    InvalidTaskPositionError,
    TaskAlreadyInBoardError,
    TaskNotInBoardError,
)
from app.features.taskboards.schemas import (
    TaskboardCreate,
    TaskboardListRead,
    TaskboardListResponse,
    TaskboardUpdate,
)
from app.models.db import Project, Task, Taskboard, TaskboardTask, User
from app.shared.exceptions import ProjectNotFoundError, TaskNotFoundError


def create_taskboard(
    db: Session,
    user: User,
    payload: TaskboardCreate,
) -> Taskboard:
    if user.active_project is None or user.active_project.deleted_at is not None:
        raise ProjectNotFoundError("User must have an active project")

    project = db.execute(
        select(Project).where(
            Project.id == user.active_project.id,
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(
            f"Active project {user.active_project.public_id} not found"
        )

    board = Taskboard(
        name=payload.name,
        description=payload.description,
        color=payload.color,
        project_id=project.id,
    )

    db.add(board)
    db.flush()
    db.refresh(board)

    return board


def update_taskboard(
    db: Session,
    board: Taskboard,
    payload: TaskboardUpdate,
) -> Taskboard:
    if "name" in payload.model_fields_set and payload.name:
        board.name = payload.name
    if "description" in payload.model_fields_set:
        board.description = payload.description or ""
    if "color" in payload.model_fields_set:
        board.color = payload.color

    db.flush()
    db.refresh(board)

    return board


def list_taskboards(
    db: Session,
    project: Project,
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
            (Task.id == TaskboardTask.task_id) & Task.deleted_at.is_(None),
        )
        .options(
            # suppress joined project loading in aggregate query
            raiseload(Taskboard.project)
        )
        .where(
            Taskboard.project_id == project.id,
            Taskboard.deleted_at.is_(None),
        )
        .group_by(Taskboard.id)
        .order_by(
            Taskboard.created_at.asc(),
            Taskboard.public_id.asc(),
        )
    )

    rows = db.execute(stmt).all()

    return TaskboardListResponse(
        items=[
            TaskboardListRead(
                public_id=taskboard.public_id,
                name=taskboard.name,
                description=taskboard.description,
                color=taskboard.color,
                project_public_id=project.public_id,
                task_count=task_count,
            )
            for taskboard, task_count in rows
        ],
    )


def delete_taskboard(
    db: Session,
    board: Taskboard,
    user: User,
) -> None:
    board.soft_delete(deleted_by=user.id)
    db.flush()


def add_task_to_board(
    db: Session,
    board: Taskboard,
    task: Task,
    position: int | None = None,
) -> TaskboardTask:
    if task.project_id != board.project_id:
        raise TaskNotFoundError(f"Task with public_id {task.public_id} not found")

    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task.id,
    )
    existing = db.execute(stmt).scalar_one_or_none()

    if existing is not None:
        raise TaskAlreadyInBoardError(f"Task {task.public_id} is already in this board")

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
    db.flush()
    db.refresh(association)

    return association


def remove_task_from_board(
    db: Session,
    board: Taskboard,
    task: Task,
) -> None:
    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task.id,
    )
    association = db.execute(stmt).scalar_one_or_none()

    if association is None:
        raise TaskAlreadyInBoardError(f"Task {task.public_id} is not in this board")

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


def reposition_task_in_board(
    db: Session,
    board: Taskboard,
    task: Task,
    position: int,
) -> None:
    if task.project_id != board.project_id:
        raise TaskNotFoundError(f"Task with public_id {task.public_id} not found")

    stmt = select(TaskboardTask).where(
        TaskboardTask.taskboard_id == board.id,
        TaskboardTask.task_id == task.id,
    )
    association = db.execute(stmt).scalar_one_or_none()

    if association is None:
        raise TaskNotInBoardError(
            f"Task {task.public_id} is not in board {board.public_id}"
        )

    old_position = association.position

    if old_position == position:
        return

    count_stmt = (
        select(func.count())
        .select_from(TaskboardTask)
        .where(TaskboardTask.taskboard_id == board.id)
    )
    task_count = db.execute(count_stmt).scalar_one()

    if position >= task_count:
        raise InvalidTaskPositionError(
            f"Invalid position {position}: board has {task_count} tasks"
        )

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
