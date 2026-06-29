from pathlib import Path

from backend.config import GUIDELINES_FOLDER

from backend.ingestion.excel_to_documents import (
    ExcelToDocuments
)

excel = list(
    Path(GUIDELINES_FOLDER).glob("*.xlsx")
)[0]

loader = ExcelToDocuments(excel)

docs = loader.load()

print("=" * 60)

print(docs[0].page_content)

print()

print(docs[0].metadata)