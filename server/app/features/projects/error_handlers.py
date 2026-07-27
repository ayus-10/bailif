from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.features.projects.exceptions import (
    DuplicateProjectError,
    ProjectError,
    ProjectNotFoundError,
)


def register(app: FastAPI) -> None:

    @app.exception_handler(ProjectError)
    async def _generic_error(_request: Request, exc: ProjectError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProjectNotFoundError)
    async def _not_found(
        _request: Request,
        exc: ProjectNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Project not found: {exc}",
            },
        )

    @app.exception_handler(DuplicateProjectError)
    async def _duplicate(
        _request: Request,
        exc: DuplicateProjectError,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": f"Project already exists: {exc}",
            },
        )
