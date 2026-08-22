from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class TaskboardNotFoundError(NotFoundError):
    error_code = "taskboard_not_found"


class TaskboardValidationError(ValidationError):
    error_code = "taskboard_validation"


class InvalidTaskPositionError(ValidationError):
    error_code = "invalid_task_position"


class TaskboardConflictError(ConflictError):
    error_code = "taskboard_conflict"


class TaskAlreadyInBoardError(ConflictError):
    error_code = "task_already_in_board"


class TaskNotInBoardError(NotFoundError):
    error_code = "task_not_in_board"
