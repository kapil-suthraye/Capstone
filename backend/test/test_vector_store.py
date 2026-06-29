from config import PDF_FOLDER, FAISS_FOLDER

from ingestion.loader import PDFLoader
from ingestion.splitter import DocumentSplitter
from ingestion.embeddings import EmbeddingModel
from ingestion.vector_store import VectorStore


print("=" * 60)
print("Medical AI Reviewer - Vector DB Test")
print("=" * 60)

# Step 1: Load PDFs
loader = PDFLoader(PDF_FOLDER)
documents = loader.load_documents()

# Step 2: Split into chunks
splitter = DocumentSplitter()
chunks = splitter.split(documents)

# Step 3: Load embedding model
embedding_model = EmbeddingModel().get_model()

# Step 4: Create vector store
vector_store = VectorStore(
    embedding_model,
    FAISS_FOLDER
)

db = vector_store.create(chunks)

print("\nVector Database Created Successfully")

print(f"Total Chunks Indexed: {len(chunks)}")