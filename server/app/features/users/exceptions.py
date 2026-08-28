from app.core.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)


class UserNotFoundError(NotFoundError):
    error_code = "user_not_found"


class UserAlreadyExistsError(ConflictError):
    error_code = "user_already_exists"


class UserPasswordHashError(InternalServerError):
    error_code = "user_password_hash_error"


class InvalidCredentialsError(UnauthorizedError):
    error_code = "invalid_credentials"
