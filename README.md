# Agentic Task Manager

A ClickUp/Loom-style task manager with an agentic assistant, backed by
CockroachDB as its persistent memory layer, deployed on AWS.

## Stack

- **Client:** Flutter (web first, desktop later — same codebase)
- **Server:** Python + FastAPI, REST + SSE
- **Database:** CockroachDB
  - Distributed Vector Indexing → semantic recall ("find things related to X")
  - Cloud Managed MCP Server → structured ad-hoc queries the agent generates on the fly
- **LLM:** Local Mistral 7B (via Ollama) during development → AWS Bedrock for submission
- **AWS:** Bedrock (agent's model), + [S3/Lambda/etc. — fill in what you actually use]

## Architecture

```
Flutter client  ──HTTP/SSE──>  FastAPI server  ──>  CockroachDB
                                     │                  ├─ tasks table (CRUD)
                                     │                  ├─ vector index (semantic search)
                                     ├──> MCP Server ──>│
                                     │                  └─ (structured queries)
                                     └──> Bedrock (LLM)
```

## Repo layout

```
server/   FastAPI backend — see server/README.md
client/   Flutter frontend — see client/README.md
```

## Quickstart

1. Spin up a CockroachDB cluster (local `cockroach demo` or CockroachDB Cloud).
2. `cd server && pip install -r requirements.txt`, fill in `.env`, run `uvicorn app.main:app --reload`.
3. `cd client && flutter pub get && flutter run -d chrome`.

## CockroachDB tools used

- **Distributed Vector Indexing** — `server/app/agent/tools/vector_search.py` — semantic memory over task history.
- **Cloud Managed MCP Server** — `server/app/agent/tools/mcp_client.py` — the agent runs structured, filtered queries it generates from natural language, without hardcoded endpoints for every possible filter combination.

## AWS services used

- **Amazon Bedrock** — hosts the agent's LLM for the submitted build (`server/app/agent/llm_client.py`, `BedrockClient`).
- [Add S3 / Lambda / etc. here if you add them]
