from pathlib import Path

import fitz

from langchain_core.documents import Document


class MedicalPDFLoader:
    """
    Loads all medical record PDFs and converts them
    into LangChain Documents.
    """

    def __init__(self, pdf_folder):

        self.pdf_folder = Path(pdf_folder)

    def load(self):

        documents = []

        pdf_files = sorted(
            self.pdf_folder.glob("*.pdf")
        )

        print(f"Found {len(pdf_files)} PDF(s)")

        for pdf in pdf_files:

            print(f"Reading {pdf.name}")

            doc = fitz.open(pdf)

            for page_number in range(len(doc)):

                page = doc.load_page(page_number)

                text = page.get_text("text")

                if text.strip():

                    documents.append(

                        Document(

                            page_content=text,

                            metadata={

                                "source": pdf.name,

                                "page": page_number + 1

                            }

                        )

                    )

            doc.close()

        print(
            f"Loaded {len(documents)} pages."
        )

        return documents