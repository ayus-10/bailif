from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "cockroachdb+psycopg2://root@localhost:26257/defaultdb?sslmode=disable"
    )

    llm_provider: str = "local"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    ollama_embedding_model: str = "qwen3-embedding:4b"

    aws_region: str = "us-east-1"
    bedrock_model_id: str = ""

    mcp_server_url: str = "https://cockroachlabs.cloud/mcp"
    mcp_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
