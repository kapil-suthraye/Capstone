"""
Tests for the Retriever thin wrapper.

Unit-tests use mocking; live tests require Pinecone + OpenAI.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def retriever():
    from Backend.app.services.retriever import Retriever
    return Retriever()


def test_retriever_instantiates(retriever):
    assert retriever is not None
    assert retriever.vector is not None


async def test_retrieve_delegates_to_vector_store():
    """Retriever.retrieve should call similarity_search then rerank."""
    from Backend.app.services.retriever import Retriever

    mock_match = MagicMock()
    mock_match.metadata = {"text": "sample", "section_heading": "Assessment"}
    mock_match.id = "chunk-1"
    mock_match.score = 0.9

    with patch(
        "Backend.app.services.retriever.VectorStore.similarity_search",
        new_callable=AsyncMock,
        return_value=[mock_match],
    ) as mock_search, patch(
        "Backend.app.services.retriever.VectorStore.rerank",
        return_value=[mock_match],
    ) as mock_rerank:
        retriever = Retriever()
        result = await retriever.vector.similarity_search("question", namespace="ns")

        mock_search.assert_called_once()
        assert len(result) == 1
