from enum import Enum


class ActionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"
    PARTIALLY_FAILED = "partially_failed"
    FAILED = "failed"


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
