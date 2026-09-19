from app.features.task_edges.schemas import TaskEdgeRead
from app.features.taskboards.schemas import TaskboardRead, TaskboardTaskRead
from app.features.users.schemas import UserRead
from app.models.db import Project, Task, Taskboard, TaskEdge, User
from app.shared.schemas import ProjectRead, TaskRead


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


def task_edge_to_read(edge: TaskEdge) -> TaskEdgeRead:
    return TaskEdgeRead(
        public_id=edge.public_id,
        task_public_id=edge.task.public_id,
        depends_on_public_id=edge.depends_on.public_id,
        edge_type=edge.edge_type,
    )


def taskboard_to_read_with_tasks(taskboard: Taskboard) -> TaskboardRead:
    tasks = [
        TaskboardTaskRead(
            position=association.position,
            task=task_to_read(association.task),
        )
        for association in taskboard.task_associations
    ]
    return _taskboard_to_read(taskboard, tasks)


def taskboard_to_read(taskboard: Taskboard) -> TaskboardRead:
    return _taskboard_to_read(taskboard, [])


def _taskboard_to_read(
    taskboard: Taskboard,
    tasks: list[TaskboardTaskRead],
) -> TaskboardRead:
    return TaskboardRead(
        public_id=taskboard.public_id,
        name=taskboard.name,
        description=taskboard.description,
        color=taskboard.color,
        project_public_id=taskboard.project.public_id,
        created_at=taskboard.created_at,
        updated_at=taskboard.updated_at,
        tasks=tasks,
    )
