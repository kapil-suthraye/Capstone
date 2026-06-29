from langchain_text_splitters import RecursiveCharacterTextSplitter


class MedicalChunker:

    def __init__(

        self,

        chunk_size=1000,

        chunk_overlap=200

    ):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap

        )

    def split(self, documents):

        chunks = self.splitter.split_documents(
            documents
        )

        print(f"Created {len(chunks)} chunks.")

        return chunks