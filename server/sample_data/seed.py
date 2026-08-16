import asyncio
import json
import uuid
from datetime import datetime

from app.core.database import SessionLocal
from app.models.db.project import Project
from app.models.db.task import Task, TaskDependency
from app.repositories.tasks.services import generate_task_embedding

GENERATE_EMBEDDINGS = True

# poetry run python -m sample_data.seed


def load_data(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def parse_uuid(value: str | None) -> uuid.UUID | None:
    return uuid.UUID(value) if value else None


def parse_datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


async def seed_projects(db, projects: list[dict]) -> None:
    for item in projects:
        try:
            project = Project(
                id=parse_uuid(item["id"]),
                name=item["name"],
                description=item.get("description", ""),
                icon=item.get("icon", "mdi-folder-outline"),
                color=item.get("color"),
                status=item.get("status", "active"),
            )
            db.add(project)
            db.flush()
            print(f"✅ project: {project.name}")
        except Exception as e:
            db.rollback()
            print(f"❌ project {item.get('name')}: {e}")
    db.commit()


async def seed_tasks(db, tasks: list[dict]) -> None:
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
            if GENERATE_EMBEDDINGS:
                try:
                    task.embedding = await generate_task_embedding(task)
                except Exception as e:
                    print(f"⚠️  embedding failed for {task.title}: {e}")
            db.add(task)
            db.flush()
            print(f"✅ task: {task.title}")
        except Exception as e:
            db.rollback()
            print(f"❌ task {item.get('title')}: {e}")
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
            print(f"✅ dependency: {item['task_id']} -> {item['depends_on_id']}")
        except Exception as e:
            db.rollback()
            print(f"❌ dependency {item.get('task_id')}: {e}")
    db.commit()


async def main() -> None:
    data = load_data("sample_data/filtered_data.json")
    projects = data.get("projects", [])
    tasks = data.get("tasks", [])
    dependencies = data.get("task_dependencies", [])
    db = SessionLocal()
    try:
        await seed_projects(db, projects)
        await seed_tasks(db, tasks)
        seed_dependencies(db, dependencies)
    finally:
        db.close()
    print("\nSeed complete.")


if __name__ == "__main__":
    asyncio.run(main())
