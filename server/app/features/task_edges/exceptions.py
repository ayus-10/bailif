from app.core.exceptions import ConflictError, NotFoundError


class TaskEdgeNotFoundError(NotFoundError):
    code = "task_edge_not_found"


class DuplicateEdgeError(ConflictError):
    code = "duplicate_edge"


class CycleDetectedError(ConflictError):
    code = "cycle_detected"


class SelfEdgeError(ConflictError):
    code = "self_edge"


class TaskLevelMismatchError(ConflictError):
    code = "task_level_mismatch"
