from backend.config import GUIDELINES_FOLDER

from backend.knowledge.sheet_selector import (
    SheetSelector
)

from backend.knowledge.workbook_loader import (
    WorkbookLoader
)


class GuidelineLoader:

    def __init__(self):

        self.selector = SheetSelector()

        self.loader = WorkbookLoader(
            GUIDELINES_FOLDER
        )

    def load(
        self,
        diagnosis
    ):

        sheet = self.selector.get_sheet(
            diagnosis
        )

        if sheet is None:

            raise ValueError(
                f"No worksheet found for '{diagnosis}'."
            )

        return self.loader.load_sheet(
            sheet
        )