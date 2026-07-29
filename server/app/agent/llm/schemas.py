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
