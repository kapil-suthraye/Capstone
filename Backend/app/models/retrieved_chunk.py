from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """
    Represents a retrieved document chunk after
    Pinecone search/reranking.
    """

    chunk_id: str

    score: float

    text: str

    metadata: dict