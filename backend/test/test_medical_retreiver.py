from backend.rag.medical_retriever import MedicalRetriever

retriever = MedicalRetriever()

docs = retriever.search(

    query="Weight",

    pdf_name="medical_records_raw_v1.pdf",

    k=5

)

for doc in docs:

    print(doc.metadata)