from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


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
    type: str
    data: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}

    @field_validator("data", mode="before")
    @classmethod
    def default_missing_data(cls, v):
        return v if isinstance(v, dict) else {}


class ActionPlan(BaseModel):
    reply: str = Field(validation_alias="message")
    requires_confirmation: bool = True
    actions: list[ActionItem] = Field(default_factory=list)

    model_config = {"extra": "ignore", "populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def normalize_reply_key(cls, data: Any) -> Any:
        if isinstance(data, dict) and ("reply" in data and "message" not in data):
            data["message"] = data["reply"]
        return data

    @field_validator("actions", mode="before")
    @classmethod
    def coerce_actions_list(cls, v):
        return v if isinstance(v, list) else []

    @model_validator(mode="after")
    def drop_invalid_action_types(self):
        valid_types = {t.value for t in ActionType}
        self.actions = [a for a in self.actions if a.type in valid_types]
        return self


class ChatRequest(BaseModel):
    project_id: UUID | None = None
    message: str


class ChatResponse(BaseModel):
    action_id: str
    reply: str
    actions: list[ActionItem]
