import httpx

from app.core.config import settings


class LocalOllamaClient:
    async def generate(self, prompt: str, model: str | None = None) -> str:
        model_name = model or settings.ollama_model_primary

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            resp.raise_for_status()

            return resp.json()["response"]


class BedrockClient:
    def __init__(self):
        import boto3  # imported lazily so local dev doesn't need boto3/AWS creds

        self._client = boto3.client("bedrock-runtime", region_name=settings.aws_region)

    async def generate(self, prompt: str, model: str | None = None) -> str:
        import json as _json

        # NOTE: request/response shape depends on the specific Bedrock model.
        # This is written for a Mistral-family model on Bedrock; adjust the
        # body/parse if you pick a different model.
        body = _json.dumps({"prompt": prompt, "max_tokens": 512, "temperature": 0.2})
        response = self._client.invoke_model(
            modelId=settings.bedrock_model_id, body=body
        )
        payload = _json.loads(response["body"].read())
        return payload["outputs"][0]["text"]


def get_llm_client():
    if settings.llm_provider == "bedrock":
        return BedrockClient()
    return LocalOllamaClient()
