from typing import Any

from pydantic import BaseModel, Field

from app.agent.schemas.action_items import ActionItemUnion
from app.agent.schemas.enums import ActionStatus, ActionType


class SuggestedTask(BaseModel):
    title: str
    description: str | None = None


class TaskSuggestionRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = ""


class TaskSuggestionResponse(BaseModel):
    suggestions: list[SuggestedTask] = Field(min_length=1, max_length=7)


class SearchTasksRequest(BaseModel):
    query: str
    top_k: int = 5


class ChatRequest(BaseModel):
    message: str | None = None  # required in normal mode
    project_id: str | None = None

    # bypass-mode only
    title: str | None = None  # mode=suggest_tasks
    description: str | None = None  # mode=suggest_tasks
    query: str | None = None  # mode=search_tasks
    top_k: int = 5  # mode=search_tasks


class ChatResponse(BaseModel):
    action_id: str | None = None
    reply: str
    actions: list[ActionItemUnion] = []
    results: Any | None = None


class ActionExecutionResult(BaseModel):
    type: ActionType
    ok: bool
    result: Any | None = None
    error: str | None = None


class AcceptActionResponse(BaseModel):
    action_id: str
    status: ActionStatus
    results: list[ActionExecutionResult]
