from app.agent.llm.generation import complete
from app.agent.llm.parsing import parse_json
from app.agent.llm.schemas import (
    TaskSuggestionRequest,
    TaskSuggestionResponse,
)
from app.models.db.task import Task


def build_prompt(
    *,
    payload: TaskSuggestionRequest,
    similar_tasks: list[tuple[Task, float]],
) -> str:
    lines = [
        "You are an AI task management assistant and task planner.",
        "Your job is to break the user's task into smaller, actionable subtasks.",
        "",
        "The following existing tasks may be relevant.",
        "Avoid suggesting duplicate tasks.",
        "If an existing task already covers the user's intent, prefer recommending it instead of creating a new one.",
        "",
    ]

    if similar_tasks:
        lines.append("Relevant tasks:")
        for task, distance in similar_tasks:
            lines.append(
                f"- Title: {task.title}"
                f"\n  Status: {task.status}"
                f"\n  Description: {task.description or 'None'}"
                f"\n  Similarity Distance: {distance:.3f}"
            )
    else:
        lines.append("No relevant tasks found.")

    lines.extend(
        [
            "",
            "User's task:",
            f"Title: {payload.title}",
            f"Description: {payload.description or 'None'}",
            "",
            "Based on the existing tasks above:",
            "- Identify if this appears to duplicate or overlap an existing task.",
            "- If it overlaps, prefer recommending the existing task instead of creating a new one.",
            "- If it is distinct, break it down into smaller, actionable subtasks.",
            "",
            "Guidelines:",
            "- Return only valid JSON.",
            "- Do not include markdown, comments, or explanations.",
            "- Provide no more than 5 suggested subtasks.",
            "- Each subtask should be clear, specific, and actionable.",
            "- Arrange subtasks in a logical order.",
            "- Do not repeat the original task.",
            "- Do not add unrelated requirements or assumptions.",
            "",
            "Output format:",
            "{",
            '  "suggestions": [',
            "    {",
            '      "title": "Short task name",',
            '      "description": "A clear description of what needs to be done"',
            "    }",
            "  ]",
            "}",
        ]
    )

    return "\n".join(lines)


async def generate_task_suggestions(
    payload: TaskSuggestionRequest,
    similar_tasks: list[tuple[Task, float]] | None = None,
) -> TaskSuggestionResponse:
    prompt = build_prompt(
        payload=payload,
        similar_tasks=similar_tasks or [],
    )
    raw = await complete(prompt)
    return parse_json(raw, TaskSuggestionResponse)
