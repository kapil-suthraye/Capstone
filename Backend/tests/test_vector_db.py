"""
Tests for Pinecone index connectivity.

Requires live PINECONE_API_KEY. Skipped in offline CI with -m "not live".
"""
from __future__ import annotations

import pytest


@pytest.mark.live
def test_pinecone_index_is_reachable():
    from pinecone import Pinecone
    from Backend.app.core.config import settings

    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()

    # The response object must have a dimension attribute
    assert hasattr(stats, "dimension") or isinstance(stats, dict)
