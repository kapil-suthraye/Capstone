from pathlib import Path
import pandas as pd

from langchain_core.documents import Document


class ExcelToDocuments:
    """
    Converts Excel sheets into LangChain Documents.
    """

    def __init__(self, excel_file):

        self.excel_file = Path(excel_file)

    def load(self):

        documents = []

        workbook = pd.ExcelFile(self.excel_file)

        print(f"Sheets Found : {workbook.sheet_names}")

        for sheet in workbook.sheet_names:

            df = pd.read_excel(
                self.excel_file,
                sheet_name=sheet
            )

            df = df.fillna("")

            for index, row in df.iterrows():

                content = ""

                for column in df.columns:

                    content += f"{column}: {row[column]}\n"

                doc = Document(

                    page_content=content,

                    metadata={

                        "sheet": sheet,

                        "row": index + 2,

                        "source": self.excel_file.name

                    }

                )

                documents.append(doc)

        print(
            f"Created {len(documents)} guideline documents."
        )

        return documents