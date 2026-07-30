from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agent.schemas.enums import ActionType
from app.agent.services.task_suggestion import generate_task_suggestions
from app.agent.services.vector_search import semantic_task_search


async def execute_action(db: Session, action_type: ActionType, data: BaseModel) -> Any:
    """Dispatch a single validated action to its executor. Returns whatever
    result is relevant to hand back to the client. Raises on failure —
    caller records per-action success/failure rather than aborting the
    whole plan."""

    match action_type:
        case ActionType.CREATE_TASK:
            # TODO: return task_service.create_task(db, **data.model_dump())
            raise NotImplementedError("create_task executor not wired up")

        case ActionType.UPDATE_TASK:
            # TODO: return task_service.update_task(db, task_id=data.id, **data.model_dump(exclude={"id"}))
            raise NotImplementedError("update_task executor not wired up")

        case ActionType.DELETE_TASK:
            # TODO: task_service.delete_task(db, task_id=data.id); return {"id": data.id, "deleted": True}
            raise NotImplementedError("delete_task executor not wired up")

        case ActionType.COMPLETE_TASK:
            # TODO: return task_service.complete_task(db, task_id=data.id)
            raise NotImplementedError("complete_task executor not wired up")

        case ActionType.REOPEN_TASK:
            # TODO: return task_service.reopen_task(db, task_id=data.id)
            raise NotImplementedError("reopen_task executor not wired up")

        case ActionType.CREATE_PROJECT:
            # TODO: return project_service.create_project(db, **data.model_dump())
            raise NotImplementedError("create_project executor not wired up")

        case ActionType.UPDATE_PROJECT:
            # TODO: return project_service.update_project(db, project_id=data.id, **data.model_dump(exclude={"id"}))
            raise NotImplementedError("update_project executor not wired up")

        case ActionType.ARCHIVE_PROJECT:
            # TODO: return project_service.archive_project(db, project_id=data.id)
            raise NotImplementedError("archive_project executor not wired up")

        case ActionType.DELETE_PROJECT:
            # TODO: project_service.delete_project(db, project_id=data.id); return {"id": data.id, "deleted": True}
            raise NotImplementedError("delete_project executor not wired up")

        case ActionType.SEARCH_TASKS:
            return await semantic_task_search(db=db, query=data.query, top_k=10)

        case ActionType.SEARCH_PROJECTS:
            # Not implemented — projects have no embeddings/search infra yet.
            return {"error": "search_projects is not implemented yet"}

        case ActionType.SUGGEST_TASKS:
            similar_tasks = await semantic_task_search(
                db=db, query=data.project_id or "", top_k=5
            )
            return await generate_task_suggestions(
                payload=data, similar_tasks=similar_tasks
            )

        case ActionType.RECOMMEND_NEXT_TASK:
            # TODO: implement — no existing function referenced for this yet
            raise NotImplementedError("recommend_next_task executor not wired up")

        case _:
            raise ValueError(f"Unhandled action type: {action_type}")
