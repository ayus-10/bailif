from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.core.pagination import decode_cursor, encode_cursor
from app.features.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.models.db.project import Project


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session, filters: ProjectFilterParams) -> ProjectListResponse:
    stmt = select(Project)

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

    if filters.cursor is not None:
        cursor_created_at, cursor_id = decode_cursor(filters.cursor)

        stmt = stmt.where(
            or_(
                Project.created_at < cursor_created_at,
                and_(
                    Project.created_at == cursor_created_at,
                    Project.id < cursor_id,
                ),
            )
        )

    stmt = stmt.order_by(
        Project.created_at.desc(),
        Project.id.desc(),
    )
    stmt = stmt.limit(filters.limit + 1)

    rows = list(db.execute(stmt).scalars().all())

    next_cursor = None
    if len(rows) > filters.limit:
        rows = rows[: filters.limit]
        last = rows[-1]
        next_cursor = encode_cursor(last.created_at, last.id)

    return ProjectListResponse(
        items=[ProjectRead.model_validate(row) for row in rows],
        next_cursor=next_cursor,
    )


def update_project(
    db: Session,
    project: Project,
    payload: ProjectUpdate,
) -> Project:
    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
