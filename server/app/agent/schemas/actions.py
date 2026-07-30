from typing import Literal

from pydantic import BaseModel


class CreateProjectData(BaseModel):
    name: str
    description: str | None = None


class UpdateProjectData(BaseModel):
    id: str
    name: str | None = None
    description: str | None = None


class ArchiveProjectData(BaseModel):
    id: str


class DeleteProjectData(BaseModel):
    id: str


class CreateTaskData(BaseModel):
    title: str
    description: str | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    project_id: str | None = None


class UpdateTaskData(BaseModel):
    id: str
    title: str | None = None
    description: str | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None


class DeleteTaskData(BaseModel):
    id: str


class CompleteTaskData(BaseModel):
    id: str


class ReopenTaskData(BaseModel):
    id: str


class SearchTasksData(BaseModel):
    query: str | None = None
    project_id: str | None = None
    status: str | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None


class SearchProjectsData(BaseModel):
    query: str | None = None


class SuggestTasksData(BaseModel):
    project_id: str | None = None
    count: int | None = None


class RecommendNextTaskData(BaseModel):
    project_id: str | None = None
