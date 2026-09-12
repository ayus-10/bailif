from app.core.exceptions import InternalServerError, NotFoundError, UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    error_code = "invalid_credentials"


class UserNotFoundError(NotFoundError):
    error_code = "user_not_found"


class RefreshTokenIssuanceError(InternalServerError):
    error_code = "refresh_token_issuance_error"
