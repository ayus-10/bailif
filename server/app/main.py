from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.models
from app.api.v1 import ai, auth, projects, taskboard, tasks, users
from app.core.exceptions import CoreError

app = FastAPI(title="Bailif Server", version="0.1.0")

# TODO: replace *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth.router,
    prefix="/api/v1",
)
app.include_router(
    users.router,
    prefix="/api/v1",
)
app.include_router(
    tasks.router,
    prefix="/api/v1",
)
app.include_router(
    projects.router,
    prefix="/api/v1",
)
app.include_router(
    ai.router,
    prefix="/api/v1",
)
app.include_router(
    taskboard.router,
    prefix="/api/v1",
)


@app.exception_handler(CoreError)
async def app_error_handler(_req, exc: CoreError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
