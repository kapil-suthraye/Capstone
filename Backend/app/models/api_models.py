from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: str
    namespace: str
    filename: str
    pdf_path: str
    chunks: int
    message: str
    detected_diagnosis: Optional[str] = None


class EvaluateRequest(BaseModel):
    namespace: str
    prompt_id: str


class HealthResponse(BaseModel):
    status: str
    version: str