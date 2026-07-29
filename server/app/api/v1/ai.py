from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.llm.schemas import (
    SearchTasksRequest,
    TaskSuggestionRequest,
    TaskSuggestionResponse,
)
from app.agent.services.task_suggestion import generate_task_suggestions
from app.agent.services.vector_search import semantic_task_search
from app.core.database import get_db

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/task-suggestions", response_model=TaskSuggestionResponse)
async def suggest_tasks(
    payload: TaskSuggestionRequest,
) -> TaskSuggestionResponse:
    return await generate_task_suggestions(payload)


@router.post("/task-search")
async def search_tasks(
    request: SearchTasksRequest,
    db: Session = Depends(get_db),
):
    return await semantic_task_search(
        db=db,
        query=request.query,
        top_k=request.top_k,
    )
