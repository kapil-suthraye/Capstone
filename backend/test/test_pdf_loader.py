from backend.config import MEDICAL_RECORDS_FOLDER

from backend.ingestion.pdf_loader import (
    MedicalPDFLoader
)

loader = MedicalPDFLoader(
    MEDICAL_RECORDS_FOLDER
)

docs = loader.load()

print()

print("=" * 60)

print(docs[0].metadata)

print()

print(docs[0].page_content[:1000])