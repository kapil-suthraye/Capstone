from pinecone import Pinecone
from Backend.app.core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

print(index.describe_index_stats())