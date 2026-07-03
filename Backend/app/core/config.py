from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve to the Backend/ directory:
#   config.py  ->  core/  ->  app/  ->  Backend/
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore",
    )

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

    @property
    def cors_origins_list(self) -> List[str]:
        """Split the comma-separated CORS_ORIGINS env var into a clean list."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
