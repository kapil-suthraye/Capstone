from backend.knowledge.workbook_loader import WorkbookLoader

from backend.config import GUIDELINES_FOLDER


class SheetSelector:
    """
    Selects the most appropriate worksheet
    based on diagnosis.
    """

    def __init__(self):

        self.loader = WorkbookLoader(
            GUIDELINES_FOLDER
        )

        self.sheet_names = self.loader.get_sheet_names()

    def get_sheet(self, diagnosis: str):

        diagnosis = diagnosis.lower()

        # Ignore helper sheets
        ignored = [
            "MASTER",
            "INDEX"
        ]

        candidates = []

        for sheet in self.sheet_names:

            skip = False

            for word in ignored:

                if word.lower() in sheet.lower():

                    skip = True

                    break

            if skip:

                continue

            candidates.append(sheet)

        # Exact match

        for sheet in candidates:

            if diagnosis == sheet.lower():

                return sheet

        # Partial match

        for sheet in candidates:

            if diagnosis in sheet.lower():

                return sheet

            if sheet.lower() in diagnosis:

                return sheet

        # Synonym mapping

        synonyms = {

            "covid":"COVID-19",

            "pneumonia":"CAP",

            "chf":"CHF-ADHF",

            "heart failure":"CHF-ADHF",

            "acs":"NSTEMI-ACS",

            "nstemi":"NSTEMI-ACS",

            "copd":"AECOPD",

            "pulmonary embolism":"Pulmonary Embolism",

            "stroke":"Ischemic Stroke",

            "cva":"Ischemic Stroke",

            "septic shock":"Sepsis"

        }

        if diagnosis in synonyms:

            return synonyms[diagnosis]

        return None