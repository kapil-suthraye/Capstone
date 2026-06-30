from langchain_community.vectorstores import FAISS

from backend.config import MEDICAL_VECTOR_DB

from backend.ingestion.embeddings import EmbeddingModel


class MedicalRetriever:

    def __init__(self):

        embeddings = EmbeddingModel().get_model()

        print("Loading Medical Vector DB...")

        self.db = FAISS.load_local(

            str(MEDICAL_VECTOR_DB),

            embeddings,

            allow_dangerous_deserialization=True

        )

    def search(
        self,
        pdf_name,
        k=8
    ):

        return self.db.similarity_search(

            query="medical review",

            k=k,

            filter={

                "source": pdf_name

            }

        )