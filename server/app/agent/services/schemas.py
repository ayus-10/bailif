from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SuggestedTask(BaseModel):
    title: str
    description: str | None = None


class TaskSuggestionRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""


class TaskSuggestionResponse(BaseModel):
    suggestions: list[SuggestedTask] = Field(min_length=1, max_length=7)


class SearchTasksRequest(BaseModel):
    query: str
    top_k: int = 5


class OllamaGenerateResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    done_reason: str
    context: list[int]
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int


class ChatRequest(BaseModel):
    project_id: UUID | None = None
    message: str


class PlannedAction(BaseModel):
    type: str
    args: dict[str, Any]


class ChatResponse(BaseModel):
    action_id: str
    reply: str
    actions: list[PlannedAction]


class ActionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ActionType(str, Enum):
    CREATE_PROJECT = "create_project"
    UPDATE_PROJECT = "update_project"
    ARCHIVE_PROJECT = "archive_project"
    DELETE_PROJECT = "delete_project"

    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    COMPLETE_TASK = "complete_task"
    REOPEN_TASK = "reopen_task"

    SEARCH_TASKS = "search_tasks"
    SEARCH_PROJECTS = "search_projects"

    SUGGEST_TASKS = "suggest_tasks"
    RECOMMEND_NEXT_TASK = "recommend_next_task"


class ActionItem(BaseModel):
    type: ActionType
    data: dict[str, Any] = Field(default_factory=dict)


class ActionPlan(BaseModel):
    reply: str
    requires_confirmation: bool = True
    actions: list[ActionItem] = Field(default_factory=list)
