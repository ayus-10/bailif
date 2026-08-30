from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError
from app.features.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.models.db import User
from app.models.db.project import Project
from app.utils.date_validation import validate_project_dates


def create_project(db: Session, user: User, payload: ProjectCreate) -> Project:
    project = Project(
        **payload.model_dump(),
        user_id=user.id,
    )

    try:
        validate_project_dates(project)
    except ValueError:
        raise ValidationError()

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def update_project(
    db: Session,
    project: Project,
    payload: ProjectUpdate,
) -> Project:
    updates = payload.model_dump(exclude_unset=True)

    try:
        validate_project_dates(project, updates)
    except ValueError:
        raise ValidationError()

    for field, value in updates.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def list_projects(
    db: Session,
    user: User,
    filters: ProjectFilterParams,
) -> ProjectListResponse:
    stmt = select(Project).where(Project.user_id == user.id)
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
    if filters.archived:
        stmt = stmt.where(Project.archived_at.is_not(None))
    else:
        stmt = stmt.where(Project.archived_at.is_(None))
    stmt = stmt.order_by(
        Project.created_at.desc(),
        Project.id.desc(),
    )
    stmt = stmt.limit(5)
    rows = list(db.execute(stmt).scalars().all())
    return ProjectListResponse(
        items=[ProjectRead.model_validate(row) for row in rows],
    )


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
