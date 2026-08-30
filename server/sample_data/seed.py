import json
import uuid
from datetime import datetime

from app.core.database import SessionLocal
from app.models.db.project import Project
from app.models.db.task import Task, TaskDependency
from app.models.db.taskboard import Taskboard, TaskboardTask
from app.models.db.user import User


def load_data(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def parse_uuid(value: str | None) -> uuid.UUID | None:
    return uuid.UUID(value) if value else None


def parse_datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def seed_users(db, users: list[dict]) -> None:
    for item in users:
        try:
            user = User(
                id=parse_uuid(item["id"]),
                username=item["username"],
                password_hash=item["password_hash"],
                active_project_id=parse_uuid(item.get("active_project_id")),
            )
            db.add(user)
            db.flush()
            print(f"user: {user.username}")
        except Exception as e:
            db.rollback()
            print(f"user {item.get('username')}: {e}")

    db.commit()


def seed_projects(db, projects: list[dict]) -> None:
    for item in projects:
        try:
            project = Project(
                id=parse_uuid(item["id"]),
                user_id=parse_uuid(item["user_id"]),
                name=item["name"],
                description=item.get("description", ""),
                icon=item.get("icon", "mdi-folder-outline"),
                color=item.get("color"),
                status=item.get("status", "active"),
            )
            db.add(project)
            db.flush()
            print(f"project: {project.name}")
        except Exception as e:
            db.rollback()
            print(f"project {item.get('name')}: {e}")

    db.commit()


def seed_user_active_project(db, users: list[dict], projects: list[dict]) -> None:
    first_project_id = parse_uuid(projects[0]["id"])

    try:
        for user_item in users:
            user = db.get(User, parse_uuid(user_item["id"]))

            if user:
                user.active_project_id = first_project_id
                print(f"user {user.username}: active_project set to {first_project_id}")

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"active_project update failed: {e}")


def seed_tasks(db, tasks: list[dict]) -> None:
    for item in tasks:
        try:
            task = Task(
                id=parse_uuid(item["id"]),
                title=item["title"],
                description=item.get("description", ""),
                status=item.get("status", "open"),
                priority=item.get("priority", "medium"),
                type=item.get("type", "task"),
                tags=item.get("tags", ""),
                due_date=parse_datetime(item.get("due_date")),
                parent_id=parse_uuid(item.get("parent_id")),
                project_id=parse_uuid(item.get("project_id")),
            )

            db.add(task)
            db.flush()
            print(f"task: {task.title}")

        except Exception as e:
            db.rollback()
            print(f"task {item.get('title')}: {e}")

    db.commit()


def seed_taskboards(db, taskboards: list[dict]) -> None:
    for item in taskboards:
        try:
            taskboard = Taskboard(
                id=parse_uuid(item["id"]),
                name=item["name"],
                description=item.get("description", ""),
                color=item.get("color"),
                project_id=parse_uuid(item["project_id"]),
            )
            db.add(taskboard)
            db.flush()
            print(f"taskboard: {taskboard.name}")
        except Exception as e:
            db.rollback()
            print(f"taskboard {item.get('name')}: {e}")

    db.commit()


def seed_taskboard_tasks(db, associations: list[dict]) -> None:
    for item in associations:
        try:
            association = TaskboardTask(
                id=parse_uuid(item["id"]),
                taskboard_id=parse_uuid(item["taskboard_id"]),
                task_id=parse_uuid(item["task_id"]),
                position=item.get("position", 0),
            )
            db.add(association)
            db.flush()

            print(f"taskboard task: {item['taskboard_id']} <- {item['task_id']}")

        except Exception as e:
            db.rollback()
            print(
                f"taskboard task "
                f"{item.get('taskboard_id')} <- {item.get('task_id')}: {e}"
            )

    db.commit()


def seed_dependencies(db, dependencies: list[dict]) -> None:
    for item in dependencies:
        try:
            dependency = TaskDependency(
                task_id=parse_uuid(item["task_id"]),
                depends_on_id=parse_uuid(item["depends_on_id"]),
                dependency_type=item.get("dependency_type", "blocks"),
            )
            db.add(dependency)
            db.flush()
            print(f"dependency: {item['task_id']} -> {item['depends_on_id']}")
        except Exception as e:
            db.rollback()
            print(f"dependency {item.get('task_id')}: {e}")

    db.commit()


def main() -> None:
    data = load_data("sample_data/filtered_data.json")

    users = data.get("users", [])
    projects = data.get("projects", [])
    tasks = data.get("tasks", [])
    taskboards = data.get("taskboards", [])
    taskboard_tasks = data.get("taskboard_tasks", [])
    dependencies = data.get("task_dependencies", [])

    db = SessionLocal()

    try:
        seed_users(db, users)
        seed_projects(db, projects)
        seed_user_active_project(db, users, projects)
        seed_tasks(db, tasks)
        seed_taskboards(db, taskboards)
        seed_taskboard_tasks(db, taskboard_tasks)
        seed_dependencies(db, dependencies)
    finally:
        db.close()

    print("\nSeed complete.")


if __name__ == "__main__":
    main()
