"""
Semantic memory lookup via CockroachDB's vector index.

Flow this stub represents:
  1. Embed the user's query text (e.g. via a sentence-transformer model,
     or an embeddings endpoint on Bedrock).
  2. Run a nearest-neighbor search against the `embedding` column on
     the tasks table (see app/db/models.py).
  3. Return the closest matching rows.

Left unimplemented on purpose — plug in your embedding model + the
actual CockroachDB vector query (cosine distance / L2, whichever your
cluster's syntax uses) once your schema is finalized.
"""

from sqlalchemy import text

from app.db.database import SessionLocal


def semantic_task_search(query: str, limit: int = 5) -> list[dict]:
    # embedding = embed(query)   # <- your embedding model call goes here
    with SessionLocal() as session:
        # Placeholder query — replace with a real ORDER BY <-> embedding query
        # once the embedding column + index exist, e.g.:
        # SELECT * FROM tasks ORDER BY embedding <-> :query_embedding LIMIT :limit
        result = session.execute(
            text("SELECT id, title, description FROM tasks LIMIT :limit"),
            {"limit": limit},
        )
        rows = result.mappings().all()
        return [dict(r) for r in rows]
