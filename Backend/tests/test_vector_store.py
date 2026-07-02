import asyncio

from Backend.app.services.vector_store import VectorStore
from Backend.app.services.ingestion_service import IngestionService


async def main():

    ingestion = IngestionService()

    chunks = ingestion.ingest(

        "medical_records/sample.pdf"

    )

    store = VectorStore()

    await store.upsert_chunks(

        chunks,

        namespace="sample",

    )

    docs = await store.retrieve(

        query="Does patient have congestive heart failure?",

        namespace="sample",

    )

    print()

    print("=" * 80)

    print("Retrieved")

    print("=" * 80)

    for doc in docs:

        print(doc.metadata["section_heading"])

        print(doc.metadata["text"][:300])

        print()


asyncio.run(main())