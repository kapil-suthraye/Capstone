from typing import List

from pydantic import BaseModel


class EvidenceItem(BaseModel):

    finding: str

    source: str

    page: int


class ReviewResponse(BaseModel):

    claim_id: str

    diagnosis: str

    summary: str

    evidence: List[EvidenceItem]

    missing_documentation: List[str]

    recommendation: str

    confidence: float