from Backend.app.services.ingestion_service import IngestionService

service = IngestionService()

chunks = service.ingest(
    pdf_path="medical_records/sample.pdf",
    namespace="test_namespace"
)

print(f"Total Chunks: {len(chunks)}")

for chunk in chunks:
    print("-" * 80)
    print(chunk)