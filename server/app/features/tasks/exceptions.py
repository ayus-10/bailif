class TaskError(Exception):
    pass


class TaskNotFoundError(TaskError):
    pass


class DuplicateTaskError(TaskError):
    pass


class TaskValidationError(TaskError):
    pass
