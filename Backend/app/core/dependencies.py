from functools import lru_cache

from Backend.app.services.vector_store import VectorStore

from Backend.app.services.llm_service import LLMService

@lru_cache

def get_vector_store():

    return VectorStore()

@lru_cache

def get_llm():

    return LLMService()