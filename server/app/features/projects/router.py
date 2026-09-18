from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.projects import services
from app.features.projects.dependencies import get_owned_project
from app.features.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)
from app.models.db import User
from app.models.db.project import Project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Project:
    return services.create_project(db, user, payload)


@router.get(
    "",
    response_model=ProjectListResponse,
)
def list_projects(
    filters: ProjectFilterParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProjectListResponse:
    return services.list_projects(db, user, filters)


@router.get(
    "/{project_public_id}",
    response_model=ProjectRead,
)
def get_project(
    project: Project = Depends(get_owned_project),
) -> Project:
    return project


@router.patch(
    "/{project_public_id}",
    response_model=ProjectRead,
)
def update_project(
    payload: ProjectUpdate,
    project: Project = Depends(get_owned_project),
    db: Session = Depends(get_db),
) -> Project:
    return services.update_project(db, project, payload)


@router.delete(
    "/{project_public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project: Project = Depends(get_owned_project),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    services.delete_project(db, project, user)
