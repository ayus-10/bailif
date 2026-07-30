from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.agent.schemas.actions import (
    ArchiveProjectData,
    CompleteTaskData,
    CreateProjectData,
    CreateTaskData,
    DeleteProjectData,
    DeleteTaskData,
    RecommendNextTaskData,
    ReopenTaskData,
    SearchProjectsData,
    SearchTasksData,
    SuggestTasksData,
    UpdateProjectData,
    UpdateTaskData,
)
from app.agent.schemas.enums import ActionType


class CreateProjectAction(BaseModel):
    type: Literal[ActionType.CREATE_PROJECT]
    data: CreateProjectData


class UpdateProjectAction(BaseModel):
    type: Literal[ActionType.UPDATE_PROJECT]
    data: UpdateProjectData


class ArchiveProjectAction(BaseModel):
    type: Literal[ActionType.ARCHIVE_PROJECT]
    data: ArchiveProjectData


class DeleteProjectAction(BaseModel):
    type: Literal[ActionType.DELETE_PROJECT]
    data: DeleteProjectData


class CreateTaskAction(BaseModel):
    type: Literal[ActionType.CREATE_TASK]
    data: CreateTaskData


class UpdateTaskAction(BaseModel):
    type: Literal[ActionType.UPDATE_TASK]
    data: UpdateTaskData


class DeleteTaskAction(BaseModel):
    type: Literal[ActionType.DELETE_TASK]
    data: DeleteTaskData


class CompleteTaskAction(BaseModel):
    type: Literal[ActionType.COMPLETE_TASK]
    data: CompleteTaskData


class ReopenTaskAction(BaseModel):
    type: Literal[ActionType.REOPEN_TASK]
    data: ReopenTaskData


class SearchTasksAction(BaseModel):
    type: Literal[ActionType.SEARCH_TASKS]
    data: SearchTasksData


class SearchProjectsAction(BaseModel):
    type: Literal[ActionType.SEARCH_PROJECTS]
    data: SearchProjectsData


class SuggestTasksAction(BaseModel):
    type: Literal[ActionType.SUGGEST_TASKS]
    data: SuggestTasksData


class RecommendNextTaskAction(BaseModel):
    type: Literal[ActionType.RECOMMEND_NEXT_TASK]
    data: RecommendNextTaskData


ActionItemUnion = Annotated[
    (
        CreateProjectAction
        | UpdateProjectAction
        | ArchiveProjectAction
        | DeleteProjectAction
        | CreateTaskAction
        | UpdateTaskAction
        | DeleteTaskAction
        | CompleteTaskAction
        | ReopenTaskAction
        | SearchTasksAction
        | SearchProjectsAction
        | SuggestTasksAction
        | RecommendNextTaskAction
    ),
    Field(discriminator="type"),
]
