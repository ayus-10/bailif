class ProjectError(Exception):
    pass


class ProjectNotFoundError(ProjectError):
    pass


class DuplicateProjectError(ProjectError):
    pass


class ProjectValidationError(ProjectError):
    pass
