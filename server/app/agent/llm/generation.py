from app.core.config import settings

from .client import get_llm_client


async def complete(prompt: str) -> str:
    client = get_llm_client()
    return await client.generate(prompt)


async def classify(prompt: str) -> str:
    client = get_llm_client()
    return await client.generate(
        prompt,
        model=settings.ollama_model_secondary,
    )
