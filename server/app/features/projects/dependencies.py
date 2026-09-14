from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.projects.exceptions import ProjectNotFoundError
from app.models.db import User
from app.models.db.project import Project


def get_project_by_public_id(
    public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Project:
    project = db.execute(
        select(Project).where(
            Project.public_id == public_id,
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(f"Project with public_id {public_id} not found")

    return project
