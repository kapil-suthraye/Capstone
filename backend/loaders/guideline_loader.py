from pathlib import Path

import pandas as pd


class GuidelineLoader:
    """
    Loads InterQual / Nurse Guideline Excel.
    """

    def __init__(self, guideline_folder):

        self.guideline_folder = Path(
            guideline_folder
        )

    def load(self):

        excel_files = list(

            self.guideline_folder.glob("*.xlsx")

        )

        if len(excel_files) == 0:

            raise FileNotFoundError(
                "No guideline file found."
            )

        file = excel_files[0]

        print(f"Loading {file.name}")

        df = pd.read_excel(file)

        return df