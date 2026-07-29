from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.services.schemas import (
    ActionStatus,
    ChatRequest,
    ChatResponse,
    SearchTasksRequest,
    TaskSuggestionRequest,
    TaskSuggestionResponse,
)
from app.agent.services.task_suggestion import generate_task_suggestions
from app.agent.services.vector_search import semantic_task_search
from app.core.database import get_db
from app.models.db.action import Action

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/task-suggestions", response_model=TaskSuggestionResponse)
async def suggest_tasks(
    payload: TaskSuggestionRequest,
    db: Session = Depends(get_db),
) -> TaskSuggestionResponse:
    similar_tasks = await semantic_task_search(
        db=db,
        query=payload.title,
        top_k=5,
    )
    return await generate_task_suggestions(
        payload=payload,
        similar_tasks=similar_tasks,
    )


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


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    plan = await generate_action_plan(
        db=db,
        # user=current_user,
        payload=payload,
    )

    action = Action(
        # user_id=current_user.id,
        project_id=payload.project_id,
        prompt=payload.message,
        reply=plan.reply,
        plan=plan.actions,
        status=ActionStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return ChatResponse(
        action_id=str(action.id),
        reply=plan.reply,
        actions=plan.actions,
    )
