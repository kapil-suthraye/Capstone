from pydantic import BaseModel, Field

from Backend.app.models.evaluation_result import ClaimVerdict, EvaluationResult, RagasMetrics


class ClaimSummary(BaseModel):
    claim_id: str
    namespace: str
    filename: str | None = None
    pdf_path: str | None = None
    status: str
    verdict: ClaimVerdict
    final_summary: str
    confidence: float = Field(default=0, ge=0, le=100)
    reviewed_criteria: int
    valid_criteria: int
    doubtful_criteria: int
    insufficient_evidence_criteria: int
    high_risk_findings: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    ragas_metrics: RagasMetrics | None = None
    evaluation_results: list[EvaluationResult] = Field(default_factory=list)
    created_at: str
    last_updated: str
