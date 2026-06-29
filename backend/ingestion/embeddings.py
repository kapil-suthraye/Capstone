from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    def __init__(self):

        print("Loading Embedding Model...")

        self.model = HuggingFaceEmbeddings(

            model_name="BAAI/bge-base-en-v1.5",

            model_kwargs={

                "device": "cpu"

            },

            encode_kwargs={

                "normalize_embeddings": True

            }

        )

    def get_model(self):

        return self.model