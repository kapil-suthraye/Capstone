from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
# app/core/config.py -> app -> Backend

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    OPENAI_MODEL: str = "gpt-5-mini"

    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: str

    CORS_ORIGINS: str = "http://localhost:4200"
    LOG_LEVEL: str = "INFO"

    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "Medical-AI-Reviewer"

    NURSE_PROMPTS_FILE: str = "Backend/data/nurse_prompts_interqual.xlsx"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()