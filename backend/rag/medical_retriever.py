from langchain_pinecone import PineconeVectorStore

from backend.ingestion.embeddings import EmbeddingModel

from backend.config import (
    PINECONE_INDEX
)


class MedicalRetriever:

    def __init__(self):

        embeddings = EmbeddingModel().get_model()

        self.vectorstore = PineconeVectorStore(

            index_name=PINECONE_INDEX,

            embedding=embeddings

        )

    def search(

        self,

        query,

        pdf_name,

        k=8

    ):

        return self.vectorstore.similarity_search(

            query=query,

            k=k,

            filter={

                "source": pdf_name

            }

        )