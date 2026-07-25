import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agent.llm_client import get_llm_client
from app.agent.tools.mcp_client import run_structured_query
from app.agent.tools.vector_search import semantic_task_search

router = APIRouter()


class AgentQuery(BaseModel):
    message: str


@router.post("/query")
async def agent_query(payload: AgentQuery):
    """
    Streams the agent's reasoning + answer back as Server-Sent Events.
    This is intentionally simple scaffolding — swap in real tool-calling
    (function calling via your LLM provider) once the plumbing works.
    """

    async def event_stream():
        llm = get_llm_client()

        yield _sse({"stage": "thinking", "message": "Reading your request..."})

        # --- Placeholder routing logic ---
        # Real version: let the LLM decide, via tool-calling, whether this
        # needs semantic recall (vector_search) or a structured filter
        # (mcp_client). For now we do a dumb keyword check as a stand-in
        # so you have something end-to-end to demo while you wire up
        # real tool-calling.
        if any(
            word in payload.message.lower()
            for word in ["overdue", "assigned", "status", "tag"]
        ):
            yield _sse(
                {
                    "stage": "tool_call",
                    "tool": "mcp_server",
                    "message": "Running structured query...",
                }
            )
            result = await run_structured_query(payload.message)
        else:
            yield _sse(
                {
                    "stage": "tool_call",
                    "tool": "vector_search",
                    "message": "Searching memory...",
                }
            )
            result = await semantic_task_search(payload.message)

        yield _sse({"stage": "tool_result", "data": result})

        answer = await llm.generate(
            f"User asked: {payload.message}\nRelevant data: {result}\nAnswer concisely."
        )
        yield _sse({"stage": "answer", "message": answer})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"
