from pathlib import Path

import pandas as pd


class GroundTruthLoader:
    """
    Loads Ground Truth Dataset.
    """

    def __init__(self, gt_folder):

        self.gt_folder = Path(
            gt_folder
        )

    def load(self):

        excel_files = list(

            self.gt_folder.glob("*.xlsx")

        )

        if len(excel_files) == 0:

            raise FileNotFoundError(
                "Ground Truth file missing."
            )

        file = excel_files[0]

        print(f"Loading {file.name}")

        return pd.read_excel(file)