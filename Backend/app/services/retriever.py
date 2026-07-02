from Backend.app.services.vector_store import VectorStore

class Retriever:

    def __init__(self):

        self.vector=VectorStore()

    def retrieve(

        self,

        question,

        diagnosis

    ):

        matches=self.vector.similarity_search(

            question,

            diagnosis

        )

        reranked=self.vector.rerank(

            question,

            matches

        )

        return reranked