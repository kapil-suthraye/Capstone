"""
Tests for the Chunker — pure logic, no external dependencies.
"""
from __future__ import annotations

import pytest

from Backend.app.models.parsed_document import ParsedDocument
from Backend.app.models.parsed_page import ParsedPage
from Backend.app.models.parsed_line import ParsedLine
from Backend.app.services.chunking import Chunker


@pytest.fixture
def chunker() -> Chunker:
    return Chunker()


def _make_doc(text: str, page: int = 1) -> ParsedDocument:
    line = ParsedLine(text=text, font_size=11.0, font_name="Arial", x=72.0, y=700.0, is_bold=False)
    return ParsedDocument(filename="test.pdf", pages=[ParsedPage(page_number=page, lines=[line])])


def test_chunk_document_returns_chunks(chunker: Chunker):
    doc = _make_doc("Patient is admitted for acute exacerbation of COPD. " * 5)
    chunks = chunker.chunk_document(doc)
    assert len(chunks) > 0


def test_chunks_have_text(chunker: Chunker):
    doc = _make_doc("Patient has hypertension and is on lisinopril.")
    chunks = chunker.chunk_document(doc)
    for chunk in chunks:
        assert chunk.text.strip() != ""


def test_no_duplicate_chunk_ids(chunker: Chunker):
    doc = _make_doc("Discharge summary. Diagnosis: sepsis. Plan: IV antibiotics. " * 10)
    chunks = chunker.chunk_document(doc)
    ids = [c.id for c in chunks]
    assert len(ids) == len(set(ids)), "Duplicate chunk IDs found"


def test_detect_diagnosis_tag_chf(chunker: Chunker):
    assert chunker.detect_diagnosis_tag("Patient has congestive heart failure.") == "CHF"


def test_detect_diagnosis_tag_none(chunker: Chunker):
    assert chunker.detect_diagnosis_tag("Patient is stable.") is None


def test_detect_medications(chunker: Chunker):
    meds = chunker.detect_medications("Patient is on lisinopril and insulin daily.")
    assert "lisinopril" in meds
    assert "insulin" in meds


def test_detect_lab_values_returns_strings(chunker: Chunker):
    """Each detected lab value must be a string, not a tuple (capture group bug guard)."""
    labs = chunker.detect_lab_values("HGB: 10.5 WBC: 8.2")
    assert len(labs) > 0
    for lab in labs:
        assert isinstance(lab, str), f"Expected str, got {type(lab)}: {lab!r}"


def test_section_priority_known_headings(chunker: Chunker):
    assert chunker.section_priority("Assessment") == 10
    assert chunker.section_priority("Plan") == 9
    assert chunker.section_priority("Unknown Section") == 5


def test_clean_strips_extra_whitespace(chunker: Chunker):
    assert Chunker.clean("  hello   world  ") == "hello world"
