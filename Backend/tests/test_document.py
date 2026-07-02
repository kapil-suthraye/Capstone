from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.models.parsed_document import ParsedDocument

chunk = DocumentChunk(
    text="Sample clinical note",
    page_start=1,
    page_end=1,
    source_file="sample.pdf"
)

print(chunk)