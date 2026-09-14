from app.features.tasks.schemas import TaskRead
from app.features.users.schemas import UserRead
from app.models.db import Task, User


def user_to_read(user: User) -> UserRead:
    return UserRead(
        public_id=user.public_id,
        username=user.username,
        active_project_public_id=(
            user.active_project.public_id if user.active_project is not None else None
        ),
    )


def task_to_read(task: Task) -> TaskRead:
    return TaskRead(
        public_id=task.public_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        type=task.type,
        tags=task.tags,
        project_public_id=task.project.public_id,
        parent_public_id=(task.parent.public_id if task.parent is not None else None),
        start_date=task.start_date,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
