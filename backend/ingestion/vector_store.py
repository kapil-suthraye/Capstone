from langchain_community.vectorstores import FAISS

import os


class VectorStore:

    def __init__(

        self,

        embedding_model,

        index_path

    ):

        self.embedding_model = embedding_model

        self.index_path = index_path

    def create(self, chunks):

        vector_db = FAISS.from_documents(

            documents=chunks,

            embedding=self.embedding_model

        )

        vector_db.save_local(

            self.index_path

        )

        print(

            f"Vector DB saved to {self.index_path}"

        )

        return vector_db

    def load(self):

        if not os.path.exists(self.index_path):

            raise FileNotFoundError(

                "FAISS index not found."

            )

        return FAISS.load_local(

            self.index_path,

            self.embedding_model,

            allow_dangerous_deserialization=True

        )