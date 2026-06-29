from langchain_community.vectorstores import FAISS

from backend.config import FAISS_FOLDER
from backend.ingestion.embeddings import EmbeddingModel


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
        query: str,
        k: int = 5,
        with_score: bool = True
    ):
        """
        Search the FAISS vector database.

        Parameters
        ----------
        query : str
            User question

        k : int
            Number of chunks to retrieve

        with_score : bool
            Return similarity scores along with documents.

        Returns
        -------
        List[Document] or List[(Document, score)]
        """

        if with_score:

            return self.vector_db.similarity_search_with_score(
                query,
                k=k
            )

        return self.vector_db.similarity_search(
            query,
            k=k
        )