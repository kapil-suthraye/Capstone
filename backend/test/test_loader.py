from config import PDF_FOLDER

from ingestion.loader import PDFLoader

from ingestion.splitter import DocumentSplitter

loader = PDFLoader(PDF_FOLDER)

documents = loader.load_documents()

splitter = DocumentSplitter()

chunks = splitter.split(documents)

print()

print("=" * 60)

print("Chunks :", len(chunks))

print("=" * 60)

print()

print(chunks[0].page_content)

print()

print(chunks[0].metadata)