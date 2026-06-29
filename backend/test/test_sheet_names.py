from backend.config import GUIDELINES_FOLDER
from backend.knowledge.workbook_loader import WorkbookLoader

loader = WorkbookLoader(GUIDELINES_FOLDER)

print("=" * 80)
print("AVAILABLE WORKSHEETS")
print("=" * 80)

for i, sheet in enumerate(loader.get_sheet_names(), start=1):
    print(f"{i}. {sheet}")