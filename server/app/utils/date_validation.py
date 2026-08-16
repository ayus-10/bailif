from datetime import datetime, timezone

from app.models.db import Project, Task


def after(start: datetime | None, end: datetime | None) -> None:
    if start is None or end is None:
        return

    if start.tzinfo is None and end.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
        end = end.replace(tzinfo=timezone.utc)
    elif (start.tzinfo is None) != (end.tzinfo is None):
        raise ValueError("end and start must have matching timezone info")

    if end < start:
        raise ValueError("end cannot be before start")


def validate_task_dates(task: "Task", updates: dict = {}) -> None:
    start = updates.get("start_date", task.start_date)
    due = updates.get("due_date", task.due_date)
    after(start, due)


def validate_project_dates(project: "Project", updates: dict = {}) -> None:
    start = updates.get("start_date", project.start_date)
    target_end = updates.get("target_end_date", project.target_end_date)
    actual_end = updates.get("actual_end_date", project.actual_end_date)
    after(start, target_end)
    after(start, actual_end)
