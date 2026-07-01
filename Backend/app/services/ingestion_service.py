from Backend.app.services.pdf_parser import PDFParser

from Backend.app.services.chunking import Chunker

from Backend.app.services.vector_store import VectorStore

class IngestionService:

    def __init__(self):

        self.parser=PDFParser()

        self.chunker=Chunker()

        self.vector=VectorStore()

    def ingest(self,pdf):

        parsed=self.parser.parse(pdf)

        chunks=self.chunker.chunk_document(parsed)

        self.vector.upsert_chunks(chunks)

        return chunks