"""
FastAPI dependency providers.

All service instances are cached via lru_cache so only one instance per
process is ever created.  Routers inject them with Depends().
"""
from __future__ import annotations

from functools import lru_cache

from Backend.app.services.embedding_service import EmbeddingService
from Backend.app.services.ingestion_service import IngestionService
from Backend.app.services.llm_service import LLMService
from Backend.app.services.nurse_prompts import NursePromptLoader
from Backend.app.services.vector_store import VectorStore
from Backend.app.core.config import settings


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


@lru_cache
def get_vector_store() -> VectorStore:
    return VectorStore()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()


@lru_cache
def get_ingestion_service() -> IngestionService:
    return IngestionService()


@lru_cache
def get_nurse_prompt_loader() -> NursePromptLoader:
    return NursePromptLoader(settings.NURSE_PROMPTS_FILE)
