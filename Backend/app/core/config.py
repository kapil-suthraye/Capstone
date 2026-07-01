from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
# app/core/config.py -> app -> Backend

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    OPENAI_MODEL: str = "gpt-5.5"
    OPENAI_FALLBACK_MODEL: str = "gpt-5.4-mini"

    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: str

    CORS_ORIGINS: str = "http://localhost:4200"
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    RETRIEVAL_TOP_K: int = 50
    RERANK_TOP_N: int = 12

    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "Medical-AI-Reviewer"

    NURSE_PROMPTS_FILE: str = str(
        BASE_DIR.parent / "data" / "jobaids" / "nurse_prompts_interqual.xlsx"
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()
