from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db import Project, User
from app.shared.dependencies.auth import get_current_user
from app.shared.exceptions import ProjectNotFoundError


def get_owned_project(
    project_public_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Project:
    project = db.execute(
        select(Project).where(
            Project.public_id == project_public_id,
            Project.user_id == user.id,
            Project.deleted_at.is_(None),
        )
    ).scalar_one_or_none()

    if project is None:
        raise ProjectNotFoundError(
            f"Project with public_id {project_public_id} not found"
        )

    return project
