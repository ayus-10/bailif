from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class ProjectNotFoundError(NotFoundError):
    error_code = "project_not_found"


class DuplicateProjectError(ConflictError):
    error_code = "duplicate_project"


class ProjectValidationError(ValidationError):
    error_code = "invalid_project"
