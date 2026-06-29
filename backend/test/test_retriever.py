from rag.retriever import MedicalRetriever


print("=" * 60)

print("Medical AI Retriever Test")

print("=" * 60)

retriever = MedicalRetriever()

query = input("\nAsk a question: ")

results = retriever.search(query)

print()

print("=" * 60)

print("Retrieved Chunks")

print("=" * 60)

for i, doc in enumerate(results, start=1):

    print()

    print(f"Chunk {i}")

    print("-" * 50)

    print(doc.page_content[:500])

    print()

    print(doc.metadata)

    print()