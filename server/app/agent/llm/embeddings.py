import httpx

from app.core.config import settings


def get_embedding(text: str) -> list[float]:
    response = httpx.post(
        f"{settings.ollama_base_url}/api/embed",
        json={"model": settings.ollama_embedding_model, "input": text},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]
