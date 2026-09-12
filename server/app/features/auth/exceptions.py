from app.core.exceptions import InternalServerError, NotFoundError, UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    error_code = "invalid_credentials"


class UserNotFoundError(NotFoundError):
    error_code = "user_not_found"


class RefreshTokenIssuanceError(InternalServerError):
    error_code = "refresh_token_issuance_error"


class AccessTokenExpiredError(UnauthorizedError):
    error_code = "access_token_expired"


class AccessTokenInvalidError(UnauthorizedError):
    error_code = "access_token_invalid"
