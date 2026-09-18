from app.core.exceptions import ConflictError, NotFoundError


class TaskEdgeNotFoundError(NotFoundError):
    code = "task_edge_not_found"


class DuplicateDependencyError(ConflictError):
    code = "duplicate_dependency"


class CycleDetectedError(ConflictError):
    code = "cycle_detected"


class SelfDependencyError(ConflictError):
    code = "self_dependency"


class TaskLevelMismatchError(ConflictError):
    code = "task_level_mismatch"
