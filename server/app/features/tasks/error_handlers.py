from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.features.tasks.exceptions import DuplicateTaskError, TaskNotFoundError


def register(app: FastAPI) -> None:
    @app.exception_handler(TaskNotFoundError)
    async def _not_found(request: Request, exc: TaskNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(DuplicateTaskError)
    async def _duplicate(request: Request, exc: DuplicateTaskError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
