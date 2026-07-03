"""
Tests for PDFParser.

File-dependent tests are skipped when the sample PDF is not present so the
suite can run in CI without the full data directory.
"""
from __future__ import annotations

import pytest

from Backend.app.services.pdf_parser import PDFParser


SAMPLE_PDF = "data/medical_records/medical_records_raw_v1.pdf"


@pytest.fixture
def parser() -> PDFParser:
    return PDFParser()


def test_parser_instantiates(parser: PDFParser):
    assert parser is not None


@pytest.mark.skipif(
    not __import__("os").path.exists(SAMPLE_PDF),
    reason="Sample PDF not present",
)
def test_parse_returns_parsed_document(parser: PDFParser):
    from Backend.app.models.parsed_document import ParsedDocument

    doc = parser.parse(SAMPLE_PDF)
    assert isinstance(doc, ParsedDocument)
    assert doc.filename.endswith(".pdf")
    assert len(doc.pages) > 0


@pytest.mark.skipif(
    not __import__("os").path.exists(SAMPLE_PDF),
    reason="Sample PDF not present",
)
def test_parse_pages_have_lines(parser: PDFParser):
    doc = parser.parse(SAMPLE_PDF)
    total_lines = sum(len(p.lines) for p in doc.pages)
    assert total_lines > 0, "Expected at least one parsed line across all pages"
