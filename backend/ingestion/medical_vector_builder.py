from backend.config import (
    MEDICAL_RECORDS_FOLDER,
    MEDICAL_VECTOR_DB
)

from backend.ingestion.loader import PDFLoader
from backend.ingestion.splitter import DocumentSplitter
from backend.ingestion.embeddings import EmbeddingModel

from langchain_community.vectorstores import FAISS


class MedicalVectorBuilder:

    def build(self):

        print("Loading Medical PDFs...")

        loader = PDFLoader(
            MEDICAL_RECORDS_FOLDER
        )

        docs = loader.load_documents()

        splitter = DocumentSplitter()

        chunks = splitter.split(docs)

        embeddings = EmbeddingModel().get_model()

        db = FAISS.from_documents(

            chunks,

            embeddings

        )

        db.save_local(
            MEDICAL_VECTOR_DB
        )

        print("Medical Vector DB Created")