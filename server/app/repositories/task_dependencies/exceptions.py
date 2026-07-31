class TaskDependencyError(Exception):
    pass


class TaskDependencyNotFoundError(TaskDependencyError):
    pass


class DuplicateDependencyError(TaskDependencyError):
    pass


class CycleDetectedError(TaskDependencyError):
    pass


class ReferencedTaskNotFoundError(TaskDependencyError):
    pass
