from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError
from app.features.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.models.db import Task, Taskboard, User
from app.models.db.project import Project
from app.utils.date_validation import validate_datetime_range


def create_project(db: Session, user: User, payload: ProjectCreate) -> Project:
    project = Project(
        **payload.model_dump(),
        user_id=user.id,
    )

    try:
        _validate_project_dates(project)
    except ValueError as exc:
        raise ValidationError(
            "Invalid project dates: target_end_date and actual_end_date must be on or after start_date."
        ) from exc

    db.add(project)
    db.flush()
    db.refresh(project)

    return project


def update_project(
    db: Session,
    project: Project,
    payload: ProjectUpdate,
) -> Project:
    updates = payload.model_dump(exclude_unset=True)

    try:
        _validate_project_dates(project)
    except ValueError as exc:
        raise ValidationError(
            "Invalid project dates: target_end_date and actual_end_date must be on or after start_date."
        ) from exc

    for field, value in updates.items():
        setattr(project, field, value)

    db.flush()
    db.refresh(project)

    return project


def list_projects(
    db: Session,
    user: User,
    filters: ProjectFilterParams,
) -> ProjectListResponse:
    stmt = select(Project).where(
        Project.user_id == user.id,
        Project.deleted_at.is_(None),
    )

    if filters.status is not None:
        stmt = stmt.where(Project.status == filters.status)
    if filters.agent_enabled is not None:
        stmt = stmt.where(Project.agent_enabled == filters.agent_enabled)
    if filters.start_date_before is not None:
        stmt = stmt.where(Project.start_date <= filters.start_date_before)
    if filters.start_date_after is not None:
        stmt = stmt.where(Project.start_date >= filters.start_date_after)
    if filters.target_end_date_before is not None:
        stmt = stmt.where(Project.target_end_date <= filters.target_end_date_before)
    if filters.target_end_date_after is not None:
        stmt = stmt.where(Project.target_end_date >= filters.target_end_date_after)

    stmt = stmt.order_by(
        Project.created_at.desc(),
        Project.public_id.desc(),
    )
    stmt = stmt.limit(5)

    rows = list(db.execute(stmt).scalars().all())

    return ProjectListResponse(
        items=[ProjectRead.model_validate(row) for row in rows],
    )


def delete_project(db: Session, project: Project, user: User) -> None:
    project.soft_delete(deleted_by=user.id)

    db.flush()

    now = project.deleted_at

    db.execute(
        update(Task)
        .where(
            Task.project_id == project.id,
            Task.deleted_at.is_(None),
        )
        .values(deleted_at=now, deleted_by=user.id),
        execution_options={"synchronize_session": "fetch"},
    )

    db.execute(
        update(Taskboard)
        .where(
            Taskboard.project_id == project.id,
            Taskboard.deleted_at.is_(None),
        )
        .values(deleted_at=now, deleted_by=user.id),
        execution_options={"synchronize_session": "fetch"},
    )

    db.flush()


def _validate_project_dates(project: "Project", updates: dict = {}) -> None:
    start = updates.get("start_date", project.start_date)
    target_end = updates.get("target_end_date", project.target_end_date)
    actual_end = updates.get("actual_end_date", project.actual_end_date)
    validate_datetime_range(start, target_end)
    validate_datetime_range(start, actual_end)
