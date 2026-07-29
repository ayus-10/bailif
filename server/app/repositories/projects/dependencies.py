from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.projects.exceptions import ProjectNotFoundError
from app.models.db.project import Project


def get_project_by_id(
    project_id: UUID,
    db: Session = Depends(get_db),
) -> Project:
    project = db.execute(
        select(Project).where(Project.id == project_id)
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(str(project_id))

    return project
