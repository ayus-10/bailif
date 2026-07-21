# Server (FastAPI + CockroachDB)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your real values
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

- Interactive API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Local LLM (dev mode)

Install [Ollama](https://ollama.com), then:

```bash
ollama pull mistral
ollama serve
```

`LLM_PROVIDER=local` in `.env` will route agent calls to Ollama.
Flip to `LLM_PROVIDER=bedrock` (and fill in AWS creds/region) before
you submit — no other code changes needed, see `app/agent/llm_client.py`.

## What's stubbed vs. real

- `/tasks` — real CRUD against CockroachDB, works today once `DATABASE_URL` is set.
- `/agent/query` — real SSE streaming + routing logic, but the two tool
  functions (`vector_search.py`, `mcp_client.py`) have placeholder queries.
  Fill in:
  1. An embedding model call + real CockroachDB vector column/index.
  2. Real MCP server credentials from the CockroachDB Cloud Console.
