from typing import List

from pydantic import BaseModel

class SupportingEvidence(BaseModel):
    page: str
    heading: str
    score: float | None = None
    evidence: str

class EvaluationResult(BaseModel):

    answer: str

    justification: str

    supporting_evidence: List[SupportingEvidence]

    confidence: float

    guideline: str | None = None

    decision_impact: str | None = None
    
