from Backend.app.services.pdf_parser import PDFParser
from Backend.app.services.chunking import Chunker
from Backend.app.services.vector_store import VectorStore


class IngestionService:

    def __init__(self):

        self.parser = PDFParser()
        self.chunker = Chunker()
        self.vector = VectorStore()

    async def ingest(
        self,
        pdf_path: str,
        namespace: str,
    ):

        parsed = self.parser.parse(pdf_path)

        chunks = self.chunker.chunk_document(parsed)

        await self.vector.upsert_chunks(
            chunks,
            namespace=namespace,
        )

        return chunks