"""
Tests for IngestionService.

The integration test requires a real PDF and live external services.
"""
from __future__ import annotations

import os
import pytest

pytestmark = pytest.mark.asyncio

SAMPLE_PDF = "data/medical_records/medical_records_raw_v1.pdf"


@pytest.fixture
def service():
    from Backend.app.services.ingestion_service import IngestionService
    return IngestionService()


def test_ingestion_service_instantiates(service):
    assert service is not None
    assert service.parser is not None
    assert service.chunker is not None
    assert service.vector is not None


@pytest.mark.live
@pytest.mark.skipif(
    not os.path.exists(SAMPLE_PDF),
    reason="Sample PDF not present",
)
async def test_ingest_returns_chunks(service):
    from Backend.app.models.document_chunk import DocumentChunk

    chunks = await service.ingest(
        pdf_path=SAMPLE_PDF,
        namespace="pytest-ingestion-test",
    )

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    for chunk in chunks:
        assert isinstance(chunk, DocumentChunk)
        assert chunk.text.strip() != ""
