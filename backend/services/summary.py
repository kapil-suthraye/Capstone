from backend.rag.chain import MedicalRAG


class SummaryService:

    def __init__(self):

        self.rag = MedicalRAG()

    def generate_summary(self):

        question = """
Generate a structured clinical summary.

Include:

1. Patient Name

2. Age

3. Gender

4. Diagnosis

5. Admission Date

6. Discharge Date

7. Length of Stay

8. Treatment

9. Medications

10. Final Outcome

Use only the provided medical documents.

If information is unavailable, clearly state 'Not Available'.
"""

        return self.rag.ask(question)