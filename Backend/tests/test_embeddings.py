"""
Tests for EmbeddingService.

These tests make live OpenAI calls and require OPENAI_API_KEY.
Mark with -m "not live" to skip them in offline CI.
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def service():
    from Backend.app.services.embedding_service import EmbeddingService
    return EmbeddingService()


@pytest.mark.live
async def test_embed_returns_vector(service):
    vector = await service.embed("Patient has congestive heart failure.")
    assert isinstance(vector, list)
    assert len(vector) == 3072  # text-embedding-3-large dimension
    assert all(isinstance(v, float) for v in vector)


@pytest.mark.live
async def test_embed_batch_returns_correct_count(service):
    texts = [
        "Patient has CHF.",
        "Patient has diabetes.",
        "Patient has pneumonia.",
    ]
    vectors = await service.embed_batch(texts)
    assert len(vectors) == len(texts)
    for vec in vectors:
        assert len(vec) == 3072


@pytest.mark.live
async def test_embed_batch_empty_returns_empty(service):
    result = await service.embed_batch([])
    assert result == []


@pytest.mark.live
async def test_embed_large_batch_batches_correctly(service):
    # 5 texts with batch_size=2 exercises the batching loop
    texts = [f"Clinical note {i}" for i in range(5)]
    vectors = await service.embed_large_batch(texts, batch_size=2)
    assert len(vectors) == 5
