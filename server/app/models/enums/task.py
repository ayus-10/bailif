from enum import Enum


class TaskType(str, Enum):
    TASK = "task"
    SUBTASK = "subtask"
    EPIC = "epic"
    BUG = "bug"


class EdgeType(str, Enum):
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked_by"
    RELATES_TO = "relates_to"
