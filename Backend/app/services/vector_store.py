from __future__ import annotations

from typing import List, Optional

from pinecone import Pinecone
from tenacity import retry, stop_after_attempt, wait_exponential

from Backend.app.core.config import settings
from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.models.retrieved_chunk import RetrievedChunk
from Backend.app.services.embedding_service import EmbeddingService


class VectorStore:
    """
    Pinecone Vector Store

    Features
    --------
    ✓ Batch Upsert
    ✓ Namespace Support
    ✓ Metadata Filtering
    ✓ Similarity Search
    ✓ Hosted Reranking
    """

    def __init__(self):

        self.pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        self.index = self.pc.Index(
            settings.PINECONE_INDEX_NAME
        )

        self.embedder = EmbeddingService()

    ####################################################################
    # UPSERT
    ####################################################################

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=8),
    )
    async def upsert_chunks(
        self,
        chunks: List[DocumentChunk],
        namespace: str,
    ):

        if not chunks:
            return

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = await self.embedder.embed_large_batch(
            texts
        )

        vectors = []

        for chunk, embedding in zip(chunks, embeddings):

            metadata = {

                **chunk.metadata,

                "text": chunk.text,
                "source_file": chunk.source_file,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "section_heading": chunk.section_heading,
                "document_category": chunk.document_category,
                "token_count": chunk.token_count,

            }

            # Pinecone does not allow None values
            metadata = {
                key: ("" if value is None else value)
                for key, value in metadata.items()
            }

            vectors.append(

                {
                    "id": chunk.id,
                    "values": embedding,
                    "metadata": metadata,
                }

            )

        self.index.upsert(

            vectors=vectors,
            namespace=namespace,

        )

        print(
            f"Uploaded {len(vectors)} vectors to namespace {namespace}"
        )

    ####################################################################
    # SEARCH
    ####################################################################

    async def similarity_search(
    self,
    query: str,
    namespace: str,
    diagnosis_tag: Optional[str] = None,
    top_k: int = 20,
):

        embedding = await self.embedder.embed(query)

        print("\n" + "=" * 80)
        print("SIMILARITY SEARCH")
        print("=" * 80)
        print("Namespace :", namespace)
        print("Query     :", query)
        print("Diagnosis :", diagnosis_tag)

        metadata_filter = {}

        if diagnosis_tag:
            metadata_filter = {
                "diagnosis_tag": {
                    "$eq": diagnosis_tag
                }
            }

        print("Filter :", metadata_filter)

        result = self.index.query(
            namespace=namespace,
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            filter=metadata_filter if metadata_filter else None,
        )

        print()
        print("Matches Found :", len(result.matches))

        for match in result.matches:
            print("--------------------------------")
            print("Score :", match.score)
            print("Heading :", match.metadata.get("section_heading"))
            print(match.metadata.get("text", "")[:150])

        print("=" * 80)

        return result.matches

    ####################################################################
    # RERANK
    ####################################################################

    def rerank(

        self,

        query: str,

        matches,

        top_n: int = 5,

    ):

        if not matches:
            return []

        documents = []

        lookup = {}

        for match in matches:

            text = match.metadata["text"]

            documents.append(text)

            lookup[text] = match

        reranked = self.pc.inference.rerank(

            model="bge-reranker-v2-m3",

            query=query,

            documents=documents,

            top_n=min(top_n, len(documents))

        )

        final = []

        for item in reranked.data:

            text = documents[item.index]

            final.append(

                lookup[text]

            )

        return final

    ####################################################################
    # RETRIEVE
    ####################################################################

    async def retrieve(

        self,

        query: str,

        namespace: str,

        diagnosis_tag=None,

        top_k=20,

        rerank_top_n=5,

    ):

        matches = await self.similarity_search(

            query=query,

            namespace=namespace,

            diagnosis_tag=diagnosis_tag,

            top_k=top_k,

        )

        reranked = self.rerank(

            query,
            matches,
            rerank_top_n,

        )

        results = []

        for item in reranked:

            results.append(

                RetrievedChunk(

                    chunk_id=item.id,

                    score=item.score,

                    text=item.metadata["text"],

                    metadata=item.metadata,

                )

            )

        return results