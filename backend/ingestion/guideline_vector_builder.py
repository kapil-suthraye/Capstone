from pathlib import Path

from langchain_community.vectorstores import FAISS

from backend.config import (
    GUIDELINES_FOLDER,
    GUIDELINE_VECTOR_DB
)

from backend.ingestion.excel_to_documents import (
    ExcelToDocuments
)

from backend.ingestion.splitter import (
    DocumentSplitter
)

from backend.ingestion.embeddings import (
    EmbeddingModel
)


class GuidelineVectorBuilder:

    def build(self):

        excel = list(

            Path(
                GUIDELINES_FOLDER
            ).glob("*.xlsx")

        )[0]

        docs = ExcelToDocuments(
            excel
        ).load()

        splitter = DocumentSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        chunks = splitter.split(docs)

        embeddings = EmbeddingModel().get_model()

        db = FAISS.from_documents(

            chunks,

            embeddings

        )

        db.save_local(
            GUIDELINE_VECTOR_DB
        )

        print(
            "Guideline Vector DB Created."
        )