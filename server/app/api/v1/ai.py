from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.agent.schemas.api_schemas import (
    ChatRequest,
    ChatResponse,
    TaskSuggestionRequest,
)
from app.agent.schemas.enums import ActionStatus
from app.agent.services.action_execution import execute_action
from app.agent.services.plan_generation import generate_action_plan
from app.agent.services.task_suggestion import generate_task_suggestions
from app.agent.services.vector_search import semantic_search
from app.core.database import get_db
from app.models.db import Task
from app.models.db.action import Action

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    mode: Literal["suggest_tasks", "search_tasks"] | None = Query(
        default=None,
        description="Bypass the LLM planner and hit a single action directly.",
    ),
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
) -> ChatResponse:
    if mode == "search_tasks":
        if not payload.query:
            raise HTTPException(422, "query is required when mode=search_tasks")
        hits = await semantic_search(
            db=db, query=payload.query, model=Task, top_k=payload.top_k
        )
        results = [{"task": task, "score": score} for task, score in hits]
        return ChatResponse(reply="", actions=[], results=results)

    if mode == "suggest_tasks":
        if not payload.title:
            raise HTTPException(422, "title is required when mode=suggest_tasks")
        similar_tasks = await semantic_search(
            db=db, query=payload.title, model=Task, top_k=5
        )
        suggestions = await generate_task_suggestions(
            payload=TaskSuggestionRequest(
                title=payload.title, description=payload.description
            ),
            similar_tasks=similar_tasks,
        )
        return ChatResponse(reply="", actions=[], results=suggestions)

    if not payload.message:
        raise HTTPException(422, "message is required")

    plan = await generate_action_plan(
        db=db,
        # user=current_user,
        payload=payload,
    )

    results: list[dict[str, Any]] | None = None
    status = ActionStatus.PENDING

    if not plan.requires_confirmation:
        results = []
        for item in plan.actions:
            try:
                result = await execute_action(db, item.type, item.data)
                results.append({"type": item.type, "ok": True, "result": result})
            except Exception as e:
                results.append({"type": item.type, "ok": False, "error": str(e)})
        status = ActionStatus.COMPLETED

    action = Action(
        # user_id=current_user.id,
        project_id=payload.project_id,
        prompt=payload.message,
        reply=plan.reply,
        plan=[a.model_dump(mode="json") for a in plan.actions],
        status=status,
        expires_at=datetime.now(UTC) + timedelta(minutes=15),
    )
    db.add(action)
    db.commit()
    db.refresh(action)

    return ChatResponse(
        action_id=str(action.id),
        reply=plan.reply,
        actions=plan.actions,
        results=results,
    )
