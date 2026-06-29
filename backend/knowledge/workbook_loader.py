from pathlib import Path
import pandas as pd


class WorkbookLoader:

    def __init__(self, workbook_folder):

        self.workbook_folder = Path(workbook_folder)

        files = list(self.workbook_folder.glob("*.xlsx"))

        if not files:
            raise FileNotFoundError("No guideline workbook found.")

        self.workbook = files[0]

        # Load workbook once
        self.excel = pd.ExcelFile(self.workbook)

    def get_sheet_names(self):

        return self.excel.sheet_names

    def load_sheet(self, sheet_name):

        print(f"Loading worksheet: {sheet_name}")

        return pd.read_excel(
            self.workbook,
            sheet_name=sheet_name
        )