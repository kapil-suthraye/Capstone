from backend.config import MEDICAL_RECORDS_FOLDER

from backend.ingestion.pdf_loader import (
    MedicalPDFLoader
)

from backend.ingestion.chunker import (
    MedicalChunker
)

loader = MedicalPDFLoader(
    MEDICAL_RECORDS_FOLDER
)

docs = loader.load()

chunker = MedicalChunker()

chunks = chunker.split(docs)

print()

print(chunks[0].metadata)

print()

print(chunks[0].page_content)