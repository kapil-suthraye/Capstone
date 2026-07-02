from __future__ import annotations

import asyncio
from typing import List

from openai import AsyncOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

from Backend.app.core.config import settings


class EmbeddingService:
    """
    OpenAI Embedding Service

    Features
    --------
    ✓ Async
    ✓ Batch Embeddings
    ✓ Automatic Retry
    ✓ Cost Efficient
    """

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_EMBEDDING_MODEL

    ####################################################################
    # SINGLE
    ####################################################################

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
    )
    async def embed(
        self,
        text: str,
    ) -> List[float]:

        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    ####################################################################
    # BATCH
    ####################################################################

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
    )
    async def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        if not texts:
            return []

        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        embeddings = []

        for item in response.data:
            embeddings.append(item.embedding)

        return embeddings

    ####################################################################
    # LARGE BATCH
    ####################################################################

    async def embed_large_batch(
        self,
        texts: List[str],
        batch_size: int = 100,
    ) -> List[List[float]]:

        if not texts:
            return []

        embeddings = []

        for i in range(0, len(texts), batch_size):

            batch = texts[i:i + batch_size]

            vectors = await self.embed_batch(batch)

            embeddings.extend(vectors)

        return embeddings