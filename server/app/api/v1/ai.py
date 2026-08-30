from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import TypeAdapter, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.schemas.action_items import ActionItemUnion
from app.agent.schemas.api_schemas import (
    AcceptActionResponse,
    ActionExecutionResult,
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
        hits = await semantic_search(db=db, query=payload.query, top_k=payload.top_k)
        results = [{"task": task, "score": score} for task, score in hits]
        return ChatResponse(reply="", actions=[], results=results)

    if mode == "suggest_tasks":
        if not payload.title:
            raise HTTPException(422, "title is required when mode=suggest_tasks")
        similar_tasks = await semantic_search(db=db, query=payload.title, top_k=5)
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
                result = await execute_action(db, item.type)
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


@router.post("/chat/actions/{action_id}/accept", response_model=AcceptActionResponse)
async def accept_action(
    action_id: str,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
) -> AcceptActionResponse:
    action = db.execute(
        select(Action).where(Action.id == action_id)
    ).scalar_one_or_none()
    if action is None:
        raise HTTPException(404, "Action not found")

    if action.status != ActionStatus.PENDING:
        raise HTTPException(409, f"Action is not pending (status={action.status})")

    if action.expires_at < datetime.now(UTC):
        raise HTTPException(409, "Action has expired and can no longer be confirmed")

    try:
        items = [
            TypeAdapter(ActionItemUnion).validate_python(item) for item in action.plan
        ]
    except ValidationError as e:
        raise HTTPException(500, "Stored action plan failed re-validation") from e

    results: list[ActionExecutionResult] = []
    failed_count = 0

    for item in items:
        try:
            result = await execute_action(db, item.type)
            results.append(
                ActionExecutionResult(type=item.type, ok=True, result=result)
            )
        except Exception as e:
            failed_count += 1
            results.append(
                ActionExecutionResult(type=item.type, ok=False, error=str(e))
            )

    action.status = (
        ActionStatus.FAILED
        if failed_count == len(items)
        else ActionStatus.PARTIALLY_FAILED
        if failed_count > 0
        else ActionStatus.COMPLETED
    )
    db.commit()
    db.refresh(action)

    return AcceptActionResponse(
        action_id=str(action.id),
        status=ActionStatus(action.status),
        results=results,
    )
