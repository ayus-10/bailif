import uuid

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.features.taskboard.exceptions import TaskboardNotFoundError
from app.models.db import Taskboard, TaskboardTask


def get_taskboard_by_id(
    board_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Taskboard:
    board = db.get(Taskboard, board_id)
    if board is None:
        raise TaskboardNotFoundError(str(board_id))
    return board


def get_taskboard_with_tasks(
    board_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Taskboard:
    board = (
        db.query(Taskboard)
        .filter(Taskboard.id == board_id)
        .options(joinedload(Taskboard.task_associations).joinedload(TaskboardTask.task))
        .first()
    )
    if board is None:
        raise TaskboardNotFoundError(str(board_id))

    board.task_associations.sort(key=lambda a: a.position)
    return board
