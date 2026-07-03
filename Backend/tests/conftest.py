"""
Shared pytest fixtures for the Medical AI Reviewer backend test suite.
"""
from __future__ import annotations

import pytest

from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.models.parsed_document import ParsedDocument
from Backend.app.models.parsed_page import ParsedPage
from Backend.app.models.parsed_line import ParsedLine


@pytest.fixture
def sample_chunk() -> DocumentChunk:
    return DocumentChunk(
        text="Patient presents with acute congestive heart failure.",
        page_start=1,
        page_end=1,
        source_file="sample.pdf",
        section_heading="Assessment",
        token_count=10,
    )


@pytest.fixture
def sample_parsed_document() -> ParsedDocument:
    line = ParsedLine(
        text="Patient has CHF.",
        font_size=12.0,
        font_name="Arial",
        x=72.0,
        y=700.0,
        is_bold=False,
    )
    page = ParsedPage(page_number=1, lines=[line])
    return ParsedDocument(filename="sample.pdf", pages=[page])
