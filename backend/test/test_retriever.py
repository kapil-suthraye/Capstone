from backend.rag.retriever import MedicalRetriever


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

for i, (doc, score) in enumerate(results, start=1):

    print("\n" + "=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)

    print(f"Similarity Score : {score:.4f}")

    print("\nMetadata")
    print(doc.metadata)

    print("\nContent")
    print("-" * 60)
    print(doc.page_content[:500])