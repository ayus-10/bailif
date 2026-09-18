from app.core.exceptions import ConflictError, ValidationError


class DuplicateProjectError(ConflictError):
    error_code = "duplicate_project"


class ProjectValidationError(ValidationError):
    error_code = "invalid_project"
