"""
Tests for VectorStore.

Live tests hit Pinecone and OpenAI; mark with -m "not live" to skip in CI.
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def store():
    from Backend.app.services.vector_store import VectorStore
    return VectorStore()


@pytest.fixture
def sample_chunks():
    from Backend.app.models.document_chunk import DocumentChunk
    return [
        DocumentChunk(
            text="Patient presents with acute exacerbation of congestive heart failure.",
            page_start=1,
            page_end=1,
            source_file="test.pdf",
            section_heading="Assessment",
        ),
        DocumentChunk(
            text="BNP levels elevated. Diuresis initiated with furosemide.",
            page_start=2,
            page_end=2,
            source_file="test.pdf",
            section_heading="Plan",
        ),
    ]


@pytest.mark.live
async def test_upsert_and_retrieve(store, sample_chunks):
    namespace = "pytest-test-namespace"

    # Upsert
    await store.upsert_chunks(sample_chunks, namespace=namespace)

    # Retrieve
    results = await store.retrieve(
        query="Does the patient have heart failure?",
        namespace=namespace,
        top_k=10,
        rerank_top_n=5,
    )

    assert len(results) > 0
    assert results[0].text is not None
    assert results[0].chunk_id is not None


@pytest.mark.live
async def test_similarity_search_returns_matches(store, sample_chunks):
    namespace = "pytest-test-namespace"
    await store.upsert_chunks(sample_chunks, namespace=namespace)

    matches = await store.similarity_search(
        query="congestive heart failure treatment",
        namespace=namespace,
        top_k=5,
    )
    assert isinstance(matches, list)
    assert len(matches) > 0


@pytest.mark.live
async def test_upsert_empty_chunks_is_noop(store):
    # Should not raise
    await store.upsert_chunks([], namespace="empty-ns")


@pytest.mark.live
async def test_rerank_empty_matches_returns_empty(store):
    result = store.rerank(query="anything", matches=[], top_n=5)
    assert result == []
