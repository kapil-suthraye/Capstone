from backend.services.summary import SummaryService

print("=" * 60)
print("Medical AI Summary Service")
print("=" * 60)

service = SummaryService()

summary = service.generate_summary()

print(summary)