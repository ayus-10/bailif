from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://aayush:1234@localhost:5432/local"

    llm_provider: str = "local"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model_primary: str = "qwen2.5:7b"
    ollama_model_secondary: str = "qwen2.5:3b"
    ollama_embedding_model: str = "qwen3-embedding:4b"

    aws_region: str = "us-east-1"
    bedrock_model_id: str = ""

    mcp_server_url: str = "https://cockroachlabs.cloud/mcp"
    mcp_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
