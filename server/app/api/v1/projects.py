from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.db.project import Project
from app.repositories.projects import services
from app.repositories.projects.dependencies import get_project_by_id
from app.repositories.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
) -> Project:
    return await services.create_project(db, payload)


@router.get(
    "",
    response_model=ProjectListResponse,
)
def list_projects(
    filters: ProjectFilterParams = Depends(),
    db: Session = Depends(get_db),
) -> ProjectListResponse:
    return services.list_projects(db, filters)


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
def get_project(
    project: Project = Depends(get_project_by_id),
) -> Project:
    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
)
async def update_project(
    payload: ProjectUpdate,
    project: Project = Depends(get_project_by_id),
    db: Session = Depends(get_db),
) -> Project:
    return await services.update_project(db, project, payload)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project: Project = Depends(get_project_by_id),
    db: Session = Depends(get_db),
) -> None:
    services.delete_project(db, project)
