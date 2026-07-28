from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.api.v1 import ai, projects, tasks

app = FastAPI(title="Bailif Server", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/health")
async def health():
    return {"status": "ok"}
