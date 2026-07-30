import asyncio
import json

from pydantic import ValidationError

from app.agent.llm.generation import complete
from app.agent.llm.parsing import parse_json_raw
from app.agent.services.schemas import ActionPlan, ActionType
from app.models.db import Project, Task

VALID_TYPES = ", ".join(f'"{t.value}"' for t in ActionType)


def _build_system_prompt(context: str) -> str:
    return f"""You are an assistant embedded in a project management app. You convert the user's natural language request into a JSON action plan.

            You MUST respond with ONLY a single JSON object. No markdown, no code fences, no explanation before or after. Just raw JSON.

            Output JSON schema:
            {{
            "message": "<short natural language reply to the user, 1-3 sentences>",
            "requires_confirmation": <true|false>,
            "actions": [
                {{
                "type": "<one of: {VALID_TYPES}>",
                "data": {{ ... action-specific fields ... }}
                }}
            ]
            }}

            Rules:
            - "actions" can be an empty list [] if the user is just asking a question or you are only searching/recommending (still fill "actions" for search/suggest/recommend types if applicable, otherwise []).
            - "requires_confirmation" must be true for any action that creates, updates, deletes, archives, completes, or reopens something. It must be false for read-only actions (search_tasks, search_projects, suggest_tasks, recommend_next_task) or if there are no actions.
            - For actions on existing tasks/projects (update_task, delete_task, complete_task, reopen_task, update_project, archive_project, delete_project), you MUST use a real "id" from the context below in "data". Never invent an id.
            - For "priority" use one of: "LOW", "MEDIUM", "HIGH".
            - Keep "message" conversational and specific to what you're proposing.
            - If the request is ambiguous or you cannot find a matching task/project in context, set "actions" to [] and use "message" to ask a clarifying question, with "requires_confirmation": false.
            - Do not include any keys other than "message", "requires_confirmation", and "actions".
            - Do not wrap the JSON in ```json or any other formatting.

            Context (existing project/task data you can reference):
            {context}
            """


def _build_context(db, project_id: str | None) -> str:
    if not project_id:
        return "No project selected."

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return "Project not found."

    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.created_at.desc())
        .limit(10)
        .all()
    )

    lines = [f'Project: id={project.id}, name="{project.name}"']
    if tasks:
        lines.append("Tasks:")
        for t in tasks:
            lines.append(
                f'- id={t.id}, title="{t.title}", status={t.status}, priority={t.priority}'
            )
    else:
        lines.append("Tasks: (none yet)")

    return "\n".join(lines)


def _parse_plan(raw_text: str) -> ActionPlan:
    data = parse_json_raw(raw_text)
    return ActionPlan(**data)


async def generate_action_plan(db, payload) -> ActionPlan:
    context = _build_context(db, getattr(payload, "project_id", None))
    system_prompt = _build_system_prompt(context)
    full_prompt = (
        f"{system_prompt}\n\nUser request: {payload.message}\n\nJSON response:"
    )

    raw = await asyncio.to_thread(complete, full_prompt)

    try:
        return _parse_plan(str(raw))
    except json.JSONDecodeError, ValueError, ValidationError:
        pass  # fall through to retry

    # One retry with a stricter corrective prompt
    fix_prompt = (
        f"{system_prompt}\n\n"
        f"User request: {payload.message}\n\n"
        f"Your previous response was not valid JSON matching the schema:\n{raw}\n\n"
        f"Respond again with ONLY the corrected raw JSON object, nothing else:"
    )
    raw_retry = await asyncio.to_thread(complete, fix_prompt)

    try:
        return _parse_plan(str(raw_retry))
    except json.JSONDecodeError, ValueError, ValidationError:
        return ActionPlan(
            reply="Sorry, I had trouble understanding that request. Could you rephrase it?",
            requires_confirmation=False,
            actions=[],
        )
