import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

# NOTE: CockroachDB's vector type/index syntax is versioned — check your
# cluster's docs for the exact column type (e.g. VECTOR(384)) and whether
# you need pgvector's SQLAlchemy type or a raw Column(Text) + migration.
# Swap this out once you've confirmed your cluster version's syntax.


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    assignee: Mapped[str] = mapped_column(String(120), default="")
    status: Mapped[str] = mapped_column(String(50), default="open")  # open, in_progress, done
    tags: Mapped[str] = mapped_column(String(255), default="")  # comma-separated for simplicity
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Placeholder for the embedding column — populate at insert/update time
    # by calling your embedding model, store as VECTOR(n) in CockroachDB.
    # embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=True)
