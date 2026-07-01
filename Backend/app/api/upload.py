import os
import uuid

from fastapi import (
    APIRouter,
    File,
    UploadFile,
)

from Backend.app.models.api_models import UploadResponse
from Backend.app.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)

UPLOAD_FOLDER = "medical_records"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_pdf(
    file: UploadFile = File(...)
):

    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(filepath, "wb") as f:
        f.write(await file.read())

    service = IngestionService()

    chunks = service.ingest(filepath)

    return UploadResponse(

        document_id=filename,

        filename=file.filename,

        chunks=len(chunks),

        message="Document uploaded successfully",

    )