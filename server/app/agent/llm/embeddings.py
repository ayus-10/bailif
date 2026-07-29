import httpx

from app.core.config import settings


async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/embed",
            json={
                "model": settings.ollama_embedding_model,
                "input": text,
            },
        )

    response.raise_for_status()
    return response.json()["embeddings"][0]
