from typing import Any

from sqlalchemy.orm import Session

from app.agent.schemas.enums import ActionType
from app.agent.services.task_suggestion import generate_task_suggestions
from app.agent.services.vector_search import semantic_search


async def execute_action(
    db: Session,
    action_type: ActionType,
) -> Any:
    match action_type:
        case ActionType.CREATE_TASK:
            raise NotImplementedError("create_task executor not wired up")

        case ActionType.UPDATE_TASK:
            raise NotImplementedError("update_task executor not wired up")

        case ActionType.DELETE_TASK:
            raise NotImplementedError("delete_task executor not wired up")

        case ActionType.COMPLETE_TASK:
            raise NotImplementedError("complete_task executor not wired up")

        case ActionType.REOPEN_TASK:
            raise NotImplementedError("reopen_task executor not wired up")

        case ActionType.CREATE_PROJECT:
            raise NotImplementedError("create_project executor not wired up")

        case ActionType.UPDATE_PROJECT:
            raise NotImplementedError("update_project executor not wired up")

        case ActionType.ARCHIVE_PROJECT:
            raise NotImplementedError("archive_project executor not wired up")

        case ActionType.DELETE_PROJECT:
            raise NotImplementedError("delete_project executor not wired up")

        case ActionType.SEARCH_TASKS:
            raise NotImplementedError("search_tasks executor not wired up")

        case ActionType.SEARCH_PROJECTS:
            raise NotImplementedError("search_projects executor not wired up")

        case ActionType.SUGGEST_TASKS:
            raise NotImplementedError("suggest_tasks executor not wired up")

        case ActionType.RECOMMEND_NEXT_TASK:
            raise NotImplementedError("recommend_next_task executor not wired up")

        case _:
            raise ValueError(f"Unhandled action type: {action_type}")
