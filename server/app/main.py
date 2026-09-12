from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.models
from app.agent.router import router as ai_router
from app.core.exceptions import CoreError
from app.features.auth.router import router as auth_router
from app.features.projects.router import router as projects_router
from app.features.taskboard.router import router as taskboard_router
from app.features.tasks.router import router as tasks_router
from app.features.users.router import router as users_router

app = FastAPI(title="Bailif Server", version="0.1.0")

# TODO: replace *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)
app.include_router(
    users_router,
    prefix="/api/v1",
)
app.include_router(
    tasks_router,
    prefix="/api/v1",
)
app.include_router(
    projects_router,
    prefix="/api/v1",
)
app.include_router(
    ai_router,
    prefix="/api/v1",
)
app.include_router(
    taskboard_router,
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
