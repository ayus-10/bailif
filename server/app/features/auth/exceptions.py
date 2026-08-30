from app.core.exceptions import NotFoundError, UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    error_code = "invalid_credentials"


class UserNotFoundError(NotFoundError):
    error_code = "user_not_found"
