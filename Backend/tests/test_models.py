"""
Tests for Pydantic models: DocumentChunk and ParsedDocument.
"""
from __future__ import annotations

from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.models.parsed_document import ParsedDocument
from Backend.app.models.parsed_line import ParsedLine
from Backend.app.models.parsed_page import ParsedPage


def test_document_chunk_defaults():
    chunk = DocumentChunk(
        text="Sample clinical note",
        page_start=1,
        page_end=1,
        source_file="sample.pdf",
    )
    assert chunk.text == "Sample clinical note"
    assert chunk.page_start == 1
    assert chunk.page_end == 1
    assert chunk.source_file == "sample.pdf"
    assert chunk.document_category == "Medical Record"
    assert chunk.section_heading == "General"
    assert chunk.chunk_type == "text"
    assert isinstance(chunk.id, str) and len(chunk.id) > 0


def test_document_chunk_id_is_unique():
    chunk_a = DocumentChunk(text="A", page_start=1, page_end=1, source_file="f.pdf")
    chunk_b = DocumentChunk(text="B", page_start=1, page_end=1, source_file="f.pdf")
    assert chunk_a.id != chunk_b.id


def test_document_chunk_metadata_defaults_to_empty_dict():
    chunk = DocumentChunk(text="x", page_start=1, page_end=1, source_file="f.pdf")
    assert chunk.metadata == {}


def test_parsed_document_structure():
    line = ParsedLine(
        text="Assessment: CHF",
        font_size=12.0,
        font_name="ArialMT",
        x=72.0,
        y=700.0,
        is_bold=False,
    )
    page = ParsedPage(page_number=1, lines=[line])
    doc = ParsedDocument(filename="record.pdf", pages=[page])

    assert doc.filename == "record.pdf"
    assert len(doc.pages) == 1
    assert doc.pages[0].page_number == 1
    assert doc.pages[0].lines[0].text == "Assessment: CHF"
