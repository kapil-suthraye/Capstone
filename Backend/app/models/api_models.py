from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: str
    namespace: str
    filename: str
    pdf_path: str
    chunks: int
    message: str


class EvaluateRequest(BaseModel):
    namespace: str
    prompt_id: str


class HealthResponse(BaseModel):
    status: str
    version: str