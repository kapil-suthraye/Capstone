import asyncio

from Backend.app.services.embedding_service import (
    EmbeddingService,
)


async def main():

    service = EmbeddingService()

    vector = await service.embed(
        "Patient has congestive heart failure."
    )

    print(len(vector))

    vectors = await service.embed_batch(

        [
            "Patient has CHF.",

            "Patient has diabetes.",

            "Patient has pneumonia.",

        ]

    )

    print(len(vectors))

    print(len(vectors[0]))


asyncio.run(main())