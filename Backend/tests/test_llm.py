"""
Tests for LLMService.

Live tests call OpenAI and Pinecone. Mark with -m "not live" to skip in CI.
"""
from __future__ import annotations

import pytest

from Backend.app.models.nurse_prompt import NursePrompt

pytestmark = pytest.mark.asyncio


@pytest.fixture
def llm_service():
    from Backend.app.services.llm_service import LLMService
    return LLMService()


@pytest.fixture
def sample_prompt() -> NursePrompt:
    return NursePrompt(
        prompt_id="TEST-001",
        job_aid="CHF-ADHF",
        category="Cardiac",
        severity_level="High",
        evaluation_prompt="Does the patient have acute congestive heart failure?",
        document_source="Discharge Summary",
        expected_finding="BNP elevation, dyspnea, edema",
        red_flag="Respiratory failure",
        guideline="InterQual CHF criteria",
        decision_impact="Approval or denial of inpatient stay",
        rag_search_keywords="heart failure BNP edema dyspnea",
    )


def test_llm_service_instantiates(llm_service):
    assert llm_service is not None
    assert llm_service.llm is not None


def test_build_context_formats_chunks(llm_service):
    from Backend.app.models.retrieved_chunk import RetrievedChunk

    chunks = [
        RetrievedChunk(
            chunk_id="abc123",
            score=0.92,
            text="Patient has CHF with BNP of 1500.",
            metadata={"section_heading": "Assessment", "page_start": 1, "page_end": 1},
        )
    ]
    context = llm_service.build_context(chunks)
    assert "Chunk-1" in context
    assert "abc123" in context
    assert "Assessment" in context


def test_normalize_confidence_scales_0_to_1(llm_service):
    assert llm_service._normalize_confidence(0.85) == 85.0


def test_normalize_confidence_clamps(llm_service):
    assert llm_service._normalize_confidence(150) == 100.0
    assert llm_service._normalize_confidence(-10) == 0.0


def test_normalize_confidence_handles_none(llm_service):
    assert llm_service._normalize_confidence(None) == 0.0


def test_normalize_verdict_valid(llm_service):
    assert llm_service._normalize_verdict("valid", "looks good", 90) == "valid"


def test_normalize_verdict_insufficient(llm_service):
    assert llm_service._normalize_verdict("insufficient_evidence", "", 10) == "insufficient_evidence"


def test_normalize_verdict_falls_back_on_answer_text(llm_service):
    result = llm_service._normalize_verdict("unknown", "insufficient documentation", 50)
    assert result == "insufficient_evidence"


def test_follow_up_actions_valid(llm_service):
    actions = llm_service._follow_up_actions(["Action A", "Action B"], "valid")
    assert actions == ["Action A", "Action B"]


def test_follow_up_actions_default_for_invalid_verdict(llm_service):
    actions = llm_service._follow_up_actions(None, "doubtful")
    assert len(actions) > 0
    assert isinstance(actions[0], str)


@pytest.mark.live
async def test_evaluate_returns_result(llm_service, sample_prompt):
    from Backend.app.models.evaluation_result import EvaluationResult

    # Uses a namespace that likely has no data — tests graceful degradation
    result = await llm_service.evaluate(
        namespace="pytest-llm-test-empty",
        prompt=sample_prompt,
    )

    assert isinstance(result, EvaluationResult)
    assert result.verdict in {"valid", "doubtful", "insufficient_evidence"}
    assert 0 <= result.confidence <= 100
    assert result.answer
    assert result.telemetry is not None
