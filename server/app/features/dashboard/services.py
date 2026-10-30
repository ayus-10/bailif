from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.features.dashboard.schemas import (
    DashboardProjectStats,
    DashboardRead,
    DashboardTaskRead,
    DashboardTaskStats,
)
from app.features.taskboards.services import list_taskboards
from app.models.db import Project, Task, User
from app.models.enums.project import ProjectStatus
from app.shared.enums import TaskStatus

LIST_LIMIT = 5

TERMINAL_STATUSES = (TaskStatus.DONE, TaskStatus.CANCELLED)


def get_dashboard(db: Session, user: User) -> DashboardRead:
    active_project = user.active_project
    taskboards = (
        list_taskboards(db, active_project).items
        if active_project is not None and active_project.deleted_at is None
        else []
    )

    return DashboardRead(
        projects=_project_stats(db, user),
        tasks=_task_stats(db, user),
        upcoming_deadlines=_upcoming_deadlines(db, user),
        recent_activity=_recent_activity(db, user),
        taskboards=taskboards,
    )


def _project_stats(db: Session, user: User) -> DashboardProjectStats:
    counts = dict(
        db.execute(
            select(Project.status, func.count(Project.id))
            .where(Project.user_id == user.id, Project.deleted_at.is_(None))
            .group_by(Project.status)
        ).all()
    )

    return DashboardProjectStats(
        total=sum(counts.values()),
        active=counts.get(ProjectStatus.ACTIVE, 0),
    )


def _task_stats(db: Session, user: User) -> DashboardTaskStats:
    is_overdue = Task.due_date < datetime.now(UTC)

    rows = db.execute(
        select(
            Task.status,
            func.count(Task.id),
            func.count(Task.id).filter(is_overdue),
        )
        .join(Project, Task.project_id == Project.id)
        .where(*_owned_task_conditions(user))
        .group_by(Task.status)
    ).all()

    by_status = {status: count for status, count, _ in rows}
    completed = by_status.get(TaskStatus.DONE, 0)
    total = sum(by_status.values())
    cancelled = by_status.get(TaskStatus.CANCELLED, 0)

    return DashboardTaskStats(
        total=total,
        completed=completed,
        pending=total - completed - cancelled,
        overdue=sum(
            overdue for status, _, overdue in rows if status not in TERMINAL_STATUSES
        ),
        by_status=by_status,
    )


def _upcoming_deadlines(db: Session, user: User) -> list[DashboardTaskRead]:
    stmt = _dashboard_tasks_query(user).where(
        Task.due_date.is_not(None),
        Task.status.not_in(TERMINAL_STATUSES),
    )
    return _read_tasks(db, stmt.order_by(Task.due_date.asc(), Task.public_id.asc()))


def _recent_activity(db: Session, user: User) -> list[DashboardTaskRead]:
    stmt = _dashboard_tasks_query(user)
    return _read_tasks(
        db, stmt.order_by(Task.updated_at.desc(), Task.public_id.desc())
    )


def _dashboard_tasks_query(user: User):
    return (
        select(
            Task.public_id,
            Task.title,
            Task.status,
            Task.priority,
            Task.due_date,
            Task.updated_at,
            Project.public_id.label("project_public_id"),
            Project.name.label("project_name"),
        )
        .join(Project, Task.project_id == Project.id)
        .where(*_owned_task_conditions(user))
    )


def _read_tasks(db: Session, stmt) -> list[DashboardTaskRead]:
    rows = db.execute(stmt.limit(LIST_LIMIT)).all()
    return [DashboardTaskRead.model_validate(row) for row in rows]


def _owned_task_conditions(user: User):
    return (
        Project.user_id == user.id,
        Project.deleted_at.is_(None),
        Task.deleted_at.is_(None),
    )
