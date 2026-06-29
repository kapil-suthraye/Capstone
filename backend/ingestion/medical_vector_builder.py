from langchain_community.vectorstores import FAISS

from backend.config import (
    MEDICAL_RECORDS_FOLDER,
    MEDICAL_VECTOR_DB
)

from backend.ingestion.pdf_loader import (
    MedicalPDFLoader
)

from backend.ingestion.chunker import (
    MedicalChunker
)

from backend.ingestion.embeddings import (
    EmbeddingModel
)


class MedicalVectorBuilder:

    def build(self):

        print("=" * 60)
        print("Building Medical Vector Database")
        print("=" * 60)

        loader = MedicalPDFLoader(
            MEDICAL_RECORDS_FOLDER
        )

        docs = loader.load()

        chunker = MedicalChunker()

        chunks = chunker.split(docs)

        embeddings = EmbeddingModel().get_model()

        vector_db = FAISS.from_documents(

            chunks,

            embeddings

        )

        vector_db.save_local(
            str(MEDICAL_VECTOR_DB)
        )

        print()

        print("Medical Vector DB Created Successfully")