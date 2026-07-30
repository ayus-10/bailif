from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.llm.embeddings import get_embedding
from app.models.db.project import Project
from app.models.db.task import Task

DEFAULT_TOP_K = 5
DEFAULT_MAX_DISTANCE = 0.35


async def semantic_search[T: Task | Project](
    db: Session,
    model: type[T],
    query: str,
    *,
    top_k: int = DEFAULT_TOP_K,
    max_distance: float = DEFAULT_MAX_DISTANCE,
) -> list[tuple[T, float]]:
    query = query.strip()

    if not query:
        return []

    query_embedding = await get_embedding(query)

    distance = model.embedding.cosine_distance(query_embedding).label("distance")

    stmt = (
        select(model, distance)
        .where(
            model.embedding.is_not(None),
            distance <= max_distance,
        )
        .order_by(distance)
        .limit(top_k)
    )

    results = db.execute(stmt).all()

    return [(obj, distance) for obj, distance in results]
