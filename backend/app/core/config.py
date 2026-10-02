from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "CORA"
    app_version: str = "0.1.0"
    debug: bool = False

    llm_api_key: str = ""
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-120b"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1024
    llm_timeout: int = 60

    chroma_persist_dir: str = str(Path(__file__).resolve().parent.parent.parent / "data" / "chroma_db")
    chroma_collection: str = "regulatory_docs"

    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 600
    chunk_overlap: int = 80
    retrieval_top_k: int = 5
    relevance_threshold: float = 0.3

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
