from langchain_community.vectorstores import FAISS

from config import FAISS_FOLDER
from ingestion.embeddings import EmbeddingModel


class MedicalRetriever:

    def __init__(self):

        print("Loading Embedding Model...")

        embeddings = EmbeddingModel().get_model()

        print("Loading FAISS Index...")

        self.vector_db = FAISS.load_local(

            FAISS_FOLDER,

            embeddings,

            allow_dangerous_deserialization=True

        )

        print("Retriever Ready.")

    def search(

        self,

        query,

        k=5

    ):

        results = self.vector_db.similarity_search(

            query,

            k=k

        )

        return results