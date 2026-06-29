from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader


class PDFLoader:

    def __init__(self, pdf_folder):

        self.pdf_folder = Path(pdf_folder)

    def load_documents(self):

        documents = []

        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        print(f"Found {len(pdf_files)} PDF(s)")

        for pdf in pdf_files:

            print(f"Reading : {pdf.name}")

            loader = PyMuPDFLoader(str(pdf))

            pages = loader.load()

            documents.extend(pages)

        print(f"Loaded {len(documents)} pages")

        return documents