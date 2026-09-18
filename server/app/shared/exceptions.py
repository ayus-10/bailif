from app.core.exceptions import NotFoundError, UnauthorizedError


class TaskNotFoundError(NotFoundError):
    error_code = "task_not_found"


class ProjectNotFoundError(NotFoundError):
    error_code = "project_not_found"


class AccessTokenExpiredError(UnauthorizedError):
    error_code = "access_token_expired"


class AccessTokenInvalidError(UnauthorizedError):
    error_code = "access_token_invalid"
