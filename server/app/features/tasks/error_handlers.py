from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.features.tasks.exceptions import (
    DuplicateTaskError,
    TaskError,
    TaskNotFoundError,
)


def register(app: FastAPI) -> None:

    @app.exception_handler(TaskNotFoundError)
    async def _generic_error(_request: Request, exc: TaskError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(TaskNotFoundError)
    async def _not_found(_request: Request, exc: TaskNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Task not found: {exc}",
            },
        )

    @app.exception_handler(DuplicateTaskError)
    async def _duplicate(_request: Request, exc: DuplicateTaskError):
        return JSONResponse(
            status_code=409,
            content={
                "detail": f"Task already exists: {exc}",
            },
        )
