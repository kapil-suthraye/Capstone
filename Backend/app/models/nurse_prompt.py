from typing import Optional

from pydantic import BaseModel, Field


class NursePrompt(BaseModel):
    """
    Represents one InterQual prompt loaded from Excel.
    """

    prompt_id: str = Field(...)

    job_aid: str = Field(...)

    category: str = Field(...)

    severity_level: Optional[str] = None

    evaluation_prompt: str

    document_source: Optional[str] = None

    expected_finding: Optional[str] = None

    red_flag: Optional[str] = None

    guideline: Optional[str] = None

    decision_impact: Optional[str] = None

    rag_search_keywords: Optional[str] = None

    sheet_name: Optional[str] = None