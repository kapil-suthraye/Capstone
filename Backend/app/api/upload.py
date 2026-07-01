import os
import uuid
import shutil

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

    # Generate a unique document id
    document_id = str(uuid.uuid4())

    # Use document id as Pinecone namespace
    namespace = document_id

    # Save uploaded PDF
    filename = f"{document_id}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    # Ingest document into Pinecone
    service = IngestionService()

    chunks = await service.ingest(
        filepath,
        namespace=namespace,
    )

    return UploadResponse(

        document_id=document_id,

        namespace=namespace,

        filename=file.filename,

        pdf_path=filepath,

        chunks=len(chunks),

        message="Document uploaded successfully"

    )