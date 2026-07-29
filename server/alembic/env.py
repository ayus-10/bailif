import os
from logging.config import fileConfig

from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import TIMESTAMP, DateTime, engine_from_config, pool

from alembic import context

load_dotenv()

from app.core.database import Base
from app.models.db.action import Action  # noqa: F401
from app.models.db.project import Project  # noqa: F401
from app.models.db.task import (  # noqa: F401
    Task,
    TaskDependency,
)

config = context.config

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set")
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def render_item(type_, obj, autogen_context):
    if type_ == "type" and isinstance(obj, Vector):
        autogen_context.imports.add("from pgvector.sqlalchemy import Vector")
        return f"Vector({obj.dim})"
    return False


def compare_type(
    _context,
    _inspected_column,
    _metadata_column,
    inspected_type,
    metadata_type,
):
    if isinstance(metadata_type, DateTime) and isinstance(inspected_type, TIMESTAMP):
        return False

    return None


def run_migrations_offline() -> None:
    """Run migrations without a live DB connection (generates raw SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        compare_type=compare_type,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live DB connection (the normal path)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            compare_type=compare_type,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
