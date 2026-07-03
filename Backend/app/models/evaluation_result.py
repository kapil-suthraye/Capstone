from typing import Literal

from pydantic import BaseModel, Field


ClaimVerdict = Literal["valid", "doubtful", "insufficient_evidence"]


class SupportingEvidence(BaseModel):
    page: str
    heading: str
    evidence: str
    score: float | None = None
    chunk_id: str | None = None


class RagasMetrics(BaseModel):
    # These are deterministic term-overlap proxies, not the official RAGAS scores.
    # Field names mirror RAGAS conventions so the schema stays compatible when the
    # production RAGAS package is wired in.  Check `scoring_method` to distinguish.
    scoring_method: str = "proxy"
    faithfulness: float | None = None
    answer_relevancy: float | None = None
    context_precision: float | None = None
    context_recall: float | None = None
    context_utilization: float | None = None
    notes: str = (
        "Proxy scores derived from term-overlap heuristics. "
        "Wire the RAGAS package against ground-truth data for production scores."
    )


class EvaluationTelemetry(BaseModel):
    trace_id: str
    model: str
    fallback_model_used: str | None = None
    latency_ms: float
    retrieved_chunks: int
    evidence_count: int
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class EvaluationResult(BaseModel):
    prompt_id: str | None = None
    category: str | None = None
    question: str | None = None
    answer: str
    verdict: ClaimVerdict = "doubtful"
    confidence: float = Field(default=0, ge=0, le=100)
    final_summary: str
    justification: str
    supporting_evidence: list[SupportingEvidence]
    follow_up_actions: list[str] = Field(default_factory=list)
    guideline: str | None = None
    decision_impact: str | None = None
    ragas_metrics: RagasMetrics | None = None
    telemetry: EvaluationTelemetry | None = None
