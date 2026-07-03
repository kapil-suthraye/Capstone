"""
Tests for NursePromptLoader.

Skipped when the Excel workbook is not present.
"""
from __future__ import annotations

import os
import pytest

from Backend.app.models.nurse_prompt import NursePrompt


PROMPTS_FILE = "data/jobaids/nurse_prompts_interqual.xlsx"

pytestmark = pytest.mark.skipif(
    not os.path.exists(PROMPTS_FILE),
    reason="Nurse prompts Excel file not present",
)


@pytest.fixture(scope="module")
def loader():
    from Backend.app.services.nurse_prompts import NursePromptLoader
    return NursePromptLoader(PROMPTS_FILE)


def test_loader_loads_prompts(loader):
    prompts = loader.get_all()
    assert isinstance(prompts, list)
    assert len(prompts) > 0, "Expected at least one prompt"


def test_each_prompt_has_required_fields(loader):
    for prompt in loader.get_all():
        assert isinstance(prompt, NursePrompt)
        assert prompt.prompt_id, "prompt_id must not be empty"
        assert prompt.evaluation_prompt, "evaluation_prompt must not be empty"


def test_get_prompt_by_id_returns_correct(loader):
    all_prompts = loader.get_all()
    first = all_prompts[0]
    found = loader.get_prompt(first.prompt_id)
    assert found is not None
    assert found.prompt_id == first.prompt_id


def test_get_prompt_unknown_id_returns_none(loader):
    assert loader.get_prompt("NONEXISTENT-ID-XYZ") is None


def test_get_job_aids_returns_sorted_list(loader):
    job_aids = loader.get_job_aids()
    assert isinstance(job_aids, list)
    assert job_aids == sorted(job_aids)


def test_get_categories_returns_list(loader):
    categories = loader.get_categories()
    assert isinstance(categories, list)
    assert len(categories) > 0


def test_search_returns_relevant_prompts(loader):
    results = loader.search("heart failure")
    # If any CHF prompts exist, search must find them
    assert isinstance(results, list)
    for p in results:
        assert "heart failure" in p.evaluation_prompt.lower()
