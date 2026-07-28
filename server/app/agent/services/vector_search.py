from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.llm.embeddings import get_embedding
from app.models.db.task import Task


def semantic_task_search(
    db: Session,
    query: str,
    limit: int = 5,
) -> list[Task]:
    query_embedding = get_embedding(query)

    stmt = (
        select(Task)
        .where(Task.embedding.is_not(None))
        .order_by(Task.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    return list(db.scalars(stmt).all())
