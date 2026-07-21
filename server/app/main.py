from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import tasks, agent

app = FastAPI(title="Agentic Task Manager API", version="0.1.0")

# Allow the Flutter web/desktop client to call this API during dev.
# Tighten this before you ship (specific origins, not "*").
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])


@app.get("/health")
async def health():
    return {"status": "ok"}
