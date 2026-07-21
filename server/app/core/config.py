from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # CockroachDB connection (Postgres wire protocol)
    database_url: str = "postgresql+asyncpg://user:password@localhost:26257/defaultdb"

    # LLM backend switch: "local" (Ollama/Mistral) or "bedrock"
    llm_provider: str = "local"

    # Local dev model (via Ollama)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"

    # AWS Bedrock (used once you swap off local dev)
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "mistral.mistral-7b-instruct-v0:2"

    # CockroachDB MCP server endpoint
    mcp_server_url: str = "https://cockroachlabs.cloud/mcp"
    mcp_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
