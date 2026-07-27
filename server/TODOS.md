# Development Roadmap

## Build Order (and Why)

### 1. Get a Raw LLM Call Working First

Build the simplest possible end-to-end flow:

```text
FastAPI Endpoint
        ↓
Ollama (qwen2.5:7b)
        ↓
Response
```

No tools, retrieval, or agent logic.

**Goal:** Create a "Hello World" pipeline that verifies:

- Ollama is running
- `qwen2.5:7b` is pulled
- `httpx` communication works
- FastAPI integration is functioning

This becomes the foundation for everything that follows.

---

### 2. Add Tool Calling

Expose your Task CRUD API as callable functions to the LLM.

Since **Qwen2.5** supports native function calling, there's no need for MCP yet.

This is the first genuinely **agentic** capability:

> "Ask a question" → "The agent performs a real action."

This is also where the following fields finally become meaningful:

- `approval_status`
- `agent_permission_level`

These should gate whether the agent can:

- commit changes automatically
- propose changes for approval

---

### 3. Populate & Query Embeddings

Generate embeddings whenever a task is created or updated.

On writes:

1. Call the embedding model.
2. Store the embedding vector.
3. Enable PostgreSQL vector search using the `<->` operator.

Once this is wired up, retrieval becomes real instead of stubbed.

---

### 4. Combine Tool Calling + Retrieval (RAG)

Build the first Retrieval-Augmented Generation workflow.

Example:

> **User:** *"What's blocking the mobile launch?"*

Flow:

1. Perform vector search.
2. Retrieve relevant tasks.
3. Inject them into the prompt.
4. Let the LLM answer using grounded project data.
5. Allow the LLM to take actions through tool calling when appropriate.

This is where the application starts feeling like a true AI project manager.

---

### 5. Add Streaming

Once the request/response loop is stable, implement response streaming for the chat UI.

Benefits:

- Lower perceived latency
- Better UX
- Enables an interactive chat dock

---

### 6. MCP (Last)

You already have:

```env
MCP_SERVER_URL=...
```

pointing to the Cockroach Labs hosted MCP server.

That means your **first MCP integration** can simply consume an existing server rather than building one yourself.

A sensible progression is:

1. Build the in-app agent loop.
2. Consume Cockroach's hosted MCP server.
3. Later, build your own MCP server exposing Patapim's tools to external clients (Claude Desktop, other agents, etc.).

---

# API Surface

## Tasks

### Create

```http
POST /tasks
```

### List

```http
GET /tasks
```

Supported query parameters:

| Parameter | Description |
|------------|-------------|
| `project_id` | Filter by project |
| `status` | Filter by status |
| `priority` | Filter by priority |
| `type` | Filter by task type |
| `assignee` | Filter by assignee |
| `tag` | Filter by tag |
| `due_before` | Due before date |
| `due_after` | Due after date |
| `parent_id` | Filter subtasks |

> **Note:** Filtering is part of CRUD, not an optional feature. Your Task Board and filters already depend on it.

---

### Retrieve

```http
GET /tasks/{id}
```

---

### Update

```http
PATCH /tasks/{id}
```

Supports partial updates.

---

### Delete

```http
DELETE /tasks/{id}
```

---

### List Subtasks

```http
GET /tasks/{id}/subtasks
```

Returns child tasks using `parent_id`.

Although this is essentially a filtered list, it deserves its own endpoint because the UI uses it frequently.

---

# Projects

### Create

```http
POST /projects
```

---

### List

```http
GET /projects
```

Supported filters:

- `status`
- `agent_enabled`

---

### Retrieve

```http
GET /projects/{id}
```

---

### Update

```http
PATCH /projects/{id}
```

---

### Delete

```http
DELETE /projects/{id}
```

---

### List Project Tasks

```http
GET /projects/{id}/tasks
```

A project-scoped task listing.

---

# Task Dependencies

### Add Dependency

```http
POST /tasks/{id}/dependencies
```

Payload:

```json
{
  "depends_on_id": "...",
  "dependency_type": "..."
}
```

---

### List Dependencies

```http
GET /tasks/{id}/dependencies
```

---

### Remove Dependency

```http
DELETE /tasks/{id}/dependencies/{dependency_id}
```

---

# Post-CRUD Roadmap

Once the CRUD surface is complete, build the following in order.

## 1. Dependency Cycle Detection

Integrate this directly into:

```http
POST /tasks/{id}/dependencies
```

Without validation, users could create cycles such as:

```text
A → B → C → A
```

which would silently break dependency graphs and Gantt charts.

This is less of a new feature and more of a required safety check.

---

## 2. Bulk Updates

```http
PATCH /tasks/bulk
```

This endpoint will become the primary interface for:

- command bar actions
- AI-driven task management
- batch operations

Agent workflows become significantly more efficient once bulk updates exist.

---

## 3. Project Summary Rollups

```http
GET /projects/{id}/summary
```

Return metrics such as:

- Task counts by status
- Completion percentage
- Overdue task count
- Other project-level KPIs

This enables the dashboard to move beyond mock data.

---

## 4. Agent Actions & Approval Flow

Suggested endpoints:

```http
POST /tasks/{id}/agent-actions
POST /tasks/{id}/approve
POST /tasks/{id}/reject
POST /tasks/decompose
```

These endpoints power the application's core AI workflow, so they shouldn't be postponed too long after CRUD is stable.

---

## 5. Semantic Search

```http
POST /tasks/search
```

Prerequisites:

- Embeddings generated on task creation/update
- Vector search operational

Before implementing this endpoint, decide whether embeddings are generated:

- inline during writes
- asynchronously via a background worker

Making that architectural decision early avoids future refactoring.

---

## 6. Recurrence Worker

Create a scheduled job that expands recurring task templates into actual task records based on each task's:

```text
recurrence_rule
```

---

## 7. Event / Outbox Pattern

Emit internal events whenever tasks or projects change.

Examples:

- Task created
- Task updated
- Task completed
- Project updated

This allows future integrations (Slack, Calendar, webhooks, etc.) to subscribe to events without requiring changes to the core business logic.
