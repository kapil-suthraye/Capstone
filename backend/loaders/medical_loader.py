from pathlib import Path


class MedicalRecordLoader:
    """
    Handles loading of medical record PDFs.
    """

    def __init__(self, medical_folder):

        self.medical_folder = Path(medical_folder)

    def get_all_records(self):

        pdfs = sorted(
            self.medical_folder.glob("*.pdf")
        )

        print(f"Found {len(pdfs)} medical record(s).")

        return pdfs

    def get_record(self, filename):

        file_path = self.medical_folder / filename

        if not file_path.exists():

            raise FileNotFoundError(
                f"{filename} not found."
            )

        return file_path