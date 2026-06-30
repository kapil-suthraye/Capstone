from pinecone import Pinecone

from langchain_pinecone import PineconeVectorStore

from backend.config import (
    MEDICAL_RECORDS_FOLDER,
    PINECONE_API_KEY,
    PINECONE_INDEX
)

from backend.ingestion.pdf_loader import MedicalPDFLoader
from backend.ingestion.chunker import MedicalChunker
from backend.ingestion.embeddings import EmbeddingModel


class MedicalVectorBuilder:

    def build(self):

        print("=" * 60)
        print("Building Pinecone Vector Database")
        print("=" * 60)

        loader = MedicalPDFLoader(
            MEDICAL_RECORDS_FOLDER
        )

        docs = loader.load()

        chunker = MedicalChunker()

        chunks = chunker.split(docs)

        embeddings = EmbeddingModel().get_model()

        pc = Pinecone(
            api_key=PINECONE_API_KEY
        )

        PineconeVectorStore.from_documents(

            documents=chunks,

            embedding=embeddings,

            index_name=PINECONE_INDEX

        )

        print()

        print("Upload Completed")