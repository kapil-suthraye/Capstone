from backend.rag.chain import MedicalRAG

print("=" * 70)
print("Medical AI Reviewer")
print("=" * 70)

rag = MedicalRAG()

while True:

    question = input("\nAsk a medical question (type exit to quit): ")

    if question.lower() == "exit":
        break

    result = rag.ask(question)

    print("\n")
    print("=" * 70)
    print("AI Answer")
    print("=" * 70)

    print(result["answer"])

    print("\n")
    print("=" * 70)
    print("Evidence Used")
    print("=" * 70)

    for i, (doc, score) in enumerate(result["documents"], start=1):

        print(f"\nDocument {i}")

        print(f"Score : {score:.4f}")

        print(doc.metadata)