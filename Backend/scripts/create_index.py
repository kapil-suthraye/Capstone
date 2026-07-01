from pinecone import Pinecone, ServerlessSpec
from Backend.app.core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

index_name = settings.PINECONE_INDEX_NAME

if index_name not in pc.list_indexes().names():

    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Index Ready")