from app.core.exceptions import ConflictError, NotFoundError


class TaskDependencyNotFoundError(NotFoundError):
    code = "task_dependency_not_found"


class DuplicateDependencyError(ConflictError):
    code = "duplicate_dependency"


class CycleDetectedError(ConflictError):
    code = "cycle_detected"


class SelfDependencyError(ConflictError):
    code = "self_dependency"
