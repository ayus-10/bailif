class CoreError(Exception):
    status_code = 500
    error_code = "internal_error"


class NotFoundError(CoreError):
    status_code = 404
    error_code = "not_found"


class ConflictError(CoreError):
    status_code = 409
    error_code = "conflict"


class ValidationError(CoreError):
    status_code = 422
    error_code = "validation_error"


class InvalidCursorError(ValidationError):
    error_code = "invalid_cursor"
