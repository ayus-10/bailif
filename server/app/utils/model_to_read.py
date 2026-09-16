from app.features.projects.schemas import ProjectRead
from app.features.taskboard.schemas import TaskboardRead, TaskboardTaskRead
from app.features.tasks.schemas import TaskRead
from app.features.users.schemas import UserRead
from app.models.db import Project, Task, Taskboard, User


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


def project_to_read(project: Project) -> ProjectRead:
    return ProjectRead(
        public_id=project.public_id,
        name=project.name,
        description=project.description,
        icon=project.icon,
        color=project.color,
        status=project.status,
        start_date=project.start_date,
        target_end_date=project.target_end_date,
        actual_end_date=project.actual_end_date,
        timezone=project.timezone,
        agent_enabled=project.agent_enabled,
        default_agent_permission_level=project.default_agent_permission_level,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def taskboard_to_read(taskboard: Taskboard) -> TaskboardRead:
    return TaskboardRead(
        public_id=taskboard.public_id,
        name=taskboard.name,
        description=taskboard.description,
        color=taskboard.color,
        project_public_id=taskboard.project.public_id,
        created_at=taskboard.created_at,
        updated_at=taskboard.updated_at,
        tasks=[
            TaskboardTaskRead(
                position=association.position,
                task=task_to_read(association.task),
            )
            for association in taskboard.task_associations
        ],
    )
