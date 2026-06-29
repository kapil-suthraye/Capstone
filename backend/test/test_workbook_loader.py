from backend.config import GUIDELINES_FOLDER

from backend.knowledge.workbook_loader import (
    WorkbookLoader
)

loader = WorkbookLoader(
    GUIDELINES_FOLDER
)

df = loader.load_sheet(
    "COVID-19"
)

print(df.head())