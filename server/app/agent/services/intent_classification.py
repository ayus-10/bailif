import json

from app.agent.llm.generation import classify
from app.agent.llm.parsing import parse_json_raw
from app.agent.schemas.enums import ActionType

VALID_TYPES = [t.value for t in ActionType]


def _build_classifier_prompt(context: str, message: str) -> str:
    types_list = "\n".join(f'- "{t}"' for t in VALID_TYPES)
    return f"""You classify a user's request into zero or more action types for a project management app.

            Respond with ONLY a JSON object, no markdown, no explanation:
            {{
            "action_types": [<one or more of the types below, or empty list if none apply>],
            "requires_confirmation": <true|false>
            }}

            Valid action types:
            {types_list}

            Rules:
            - Pick every action type that applies to the request (a single message can imply multiple actions, e.g. create a project AND a task).
            - "requires_confirmation" is true if ANY selected action creates, updates, deletes, archives, completes, or reopens something. False if all selected actions are read-only (search_tasks, search_projects, suggest_tasks, recommend_next_task), or if action_types is empty.
            - If the request is just a question or unclear, return an empty "action_types" list.

            Context:
            {context}

            User request: {message}

            JSON response:"""


async def classify_intent(context: str, message: str) -> dict:
    prompt = _build_classifier_prompt(context, message)
    raw = await classify(prompt)
    try:
        data = parse_json_raw(str(raw))
    except json.JSONDecodeError, ValueError:
        return {"action_types": [], "requires_confirmation": False}

    action_types = [t for t in data.get("action_types", []) if t in VALID_TYPES]
    return {
        "action_types": action_types,
        "requires_confirmation": bool(data.get("requires_confirmation", False)),
    }
