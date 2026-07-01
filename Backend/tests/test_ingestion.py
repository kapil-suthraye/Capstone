from Backend.app.services.ingestion_service import IngestionService

service = IngestionService()

chunks = service.ingest(
    "medical_records/sample.pdf"
)

print(f"Generated Chunks : {len(chunks)}")

for chunk in chunks[:5]:

    print("=" * 80)

    print(chunk.section_heading)

    print(chunk.page_start)

    print(chunk.token_count)

    print(chunk.metadata)

    print(chunk.text[:400])