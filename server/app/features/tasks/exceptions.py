from app.core.exceptions import ConflictError, ValidationError


class DuplicateTaskError(ConflictError):
    error_code = "duplicate_task"


class TaskValidationError(ValidationError):
    error_code = "invalid_task"
