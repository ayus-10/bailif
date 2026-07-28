from .client import get_llm_client


async def complete(prompt: str) -> str:
    client = get_llm_client()
    return await client.generate(prompt)
