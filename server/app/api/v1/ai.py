from fastapi import APIRouter

from app.agent.llm.schemas import TaskSuggestionRequest, TaskSuggestionResponse
from app.agent.services.task_suggestion import generate_task_suggestions

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/task-suggestions", response_model=TaskSuggestionResponse)
async def suggest_tasks(
    payload: TaskSuggestionRequest,
) -> TaskSuggestionResponse:
    return await generate_task_suggestions(payload)
