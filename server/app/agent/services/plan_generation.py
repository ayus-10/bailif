import json

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.llm.generation import complete
from app.agent.llm.parsing import parse_json_raw
from app.agent.schemas.planning import ActionPlan
from app.agent.services.intent_classification import classify_intent
from app.models.db import Project, Task

ACTION_DATA_SCHEMAS = {
    "create_project": '{"name": str (required), "description": str|null}',
    "update_project": '{"id": str (required, real id from context), "name": str|null, "description": str|null}',
    "archive_project": '{"id": str (required, real id from context)}',
    "delete_project": '{"id": str (required, real id from context)}',
    "create_task": '{"title": str (required), "description": str|null, "priority": "LOW"|"MEDIUM"|"HIGH", "project_id": str|null}',
    "update_task": '{"id": str (required, real id from context), "title": str|null, "description": str|null, "priority": "LOW"|"MEDIUM"|"HIGH"|null}',
    "delete_task": '{"id": str (required, real id from context)}',
    "complete_task": '{"id": str (required, real id from context)}',
    "reopen_task": '{"id": str (required, real id from context)}',
    "search_tasks": '{"query": str|null, "project_id": str|null, "status": str|null, "priority": "LOW"|"MEDIUM"|"HIGH"|null}',
    "search_projects": '{"query": str|null}',
    "suggest_tasks": '{"project_id": str|null, "count": int|null}',
    "recommend_next_task": '{"project_id": str|null}',
}


def _build_context(db, project_id: str | None) -> str:
    if not project_id:
        return "No project selected."

    project = db.execute(
        select(Project).where(Project.id == project_id)
    ).scalar_one_or_none()
    if not project:
        return "Project not found."

    tasks = (
        db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.created_at.desc())
            .limit(10)
        )
        .scalars()
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


def _build_generation_prompt(
    context: str, message: str, action_types: list[str]
) -> str:
    if not action_types:
        schemas_block = "(no actions — just answer conversationally)"
    else:
        schemas_block = "\n".join(
            f"- {t}: {ACTION_DATA_SCHEMAS[t]}" for t in action_types
        )

    return f"""You are an assistant embedded in a project management app. Generate the final JSON action plan for the user's request.

            You MUST respond with ONLY a single JSON object. No markdown, no code fences, no explanation.

            Output JSON schema:
            {{
            "reply": "<short natural language reply to the user, 1-3 sentences>",
            "requires_confirmation": <true|false>,
            "actions": [
                {{"type": "<action type>", "data": {{ ... }}}}
            ]
            }}

            Only use these action types (already decided) and their exact "data" fields:
            {schemas_block}

            Important: projects use "name" for their title field. Tasks use "title" for their title field. Never mix these up.

            Rules:
            - For actions on existing tasks/projects, you MUST use a real "id" from the context below. Never invent an id.
            - If a task belongs to a project also being created in this same plan, omit "project_id" (leave null); mention the linkage in "reply" instead.
            - Do not include any keys other than "reply", "requires_confirmation", and "actions".
            - Do not wrap the JSON in ```json or any other formatting.

            Context:
            {context}

            User request: {message}

            JSON response:"""


def _parse_plan(raw_text: str) -> ActionPlan:
    data = parse_json_raw(raw_text)
    return ActionPlan(**data)


async def generate_action_plan(db: Session, payload) -> ActionPlan:
    context = _build_context(db, getattr(payload, "project_id", None))

    intent = await classify_intent(context, payload.message)
    action_types = intent["action_types"]

    gen_prompt = _build_generation_prompt(context, payload.message, action_types)
    raw = await complete(gen_prompt)

    try:
        return _parse_plan(str(raw))
    except json.JSONDecodeError, ValueError, ValidationError:
        pass  # fall through to retry

    fix_prompt = (
        f"{gen_prompt}\n\n"
        f"Your previous response was not valid JSON matching the schema:\n{raw}\n\n"
        f"Respond again with ONLY the corrected raw JSON object, nothing else:"
    )
    raw_retry = await complete(fix_prompt)

    try:
        return _parse_plan(str(raw_retry))
    except json.JSONDecodeError, ValueError, ValidationError:
        return ActionPlan(
            reply="Sorry, I had trouble understanding that request. Could you rephrase it?",
            requires_confirmation=False,
            actions=[],
        )
