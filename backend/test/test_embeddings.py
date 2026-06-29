from backend.ingestion.embeddings import (
    EmbeddingModel
)

model = EmbeddingModel().get_model()

vector = model.embed_query(
    "Patient admitted with fever"
)

print(len(vector))