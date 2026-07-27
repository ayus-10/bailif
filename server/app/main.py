from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features import tasks

app = FastAPI(title="Bailif Server", version="0.1.0")

# TODO: allow specific origins, not "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)

tasks.register_error_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
