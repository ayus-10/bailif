from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class TaskNotFoundError(NotFoundError):
    error_code = "task_not_found"


class DuplicateTaskError(ConflictError):
    error_code = "duplicate_task"


class TaskValidationError(ValidationError):
    error_code = "invalid_task"
