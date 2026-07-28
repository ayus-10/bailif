from app.agent.llm.generation import complete
from app.agent.llm.parsing import parse_json
from app.agent.llm.schemas import (
    TaskSuggestionRequest,
    TaskSuggestionResponse,
)

"""
A couple of implementation details make it feel polished:
- Debounce requests (e.g. 500–1000 ms after typing stops).
- Cancel the previous request if the user types again (using AbortController in the browser).
- Include a request ID/version so if an older response arrives after a newer one, you ignore it.
"""

TASK_SUGGESTION_PROMPT = """
You are a task planner. Your job is to break a user's task into smaller, actionable subtasks.

Task:
Title: {title}
Description: {description}

Guidelines:
- Return only valid JSON.
- Do not include markdown, comments, or explanations.
- Provide no more than 5 suggested subtasks.
- Each subtask should be clear, specific, and actionable.
- Arrange subtasks in a logical order.
- Do not repeat the original task.
- Do not add unrelated requirements or assumptions.

Output format:
{{
  "suggestions": [
    {{
      "title": "Short task name",
      "description": "A clear description of what needs to be done"
    }}
  ]
}}
"""


async def generate_task_suggestions(
    payload: TaskSuggestionRequest,
) -> TaskSuggestionResponse:
    prompt = TASK_SUGGESTION_PROMPT.format(
        title=payload.title,
        description=payload.description,
    )

    raw = await complete(prompt)

    return parse_json(raw, TaskSuggestionResponse)
