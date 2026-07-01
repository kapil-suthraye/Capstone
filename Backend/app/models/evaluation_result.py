from typing import List

from pydantic import BaseModel


class EvaluationResult(BaseModel):

    answer: str

    justification: str

    supporting_evidence: List[str]

    confidence: float

    guideline: str | None = None

    decision_impact: str | None = None