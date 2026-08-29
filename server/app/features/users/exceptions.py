from app.core.exceptions import (
    ConflictError,
    InternalServerError,
)


class UserAlreadyExistsError(ConflictError):
    error_code = "user_already_exists"


class UserPasswordHashError(InternalServerError):
    error_code = "user_password_hash_error"
