from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from openpyxl import load_workbook

from Backend.app.models.nurse_prompt import NursePrompt


class NursePromptLoader:

    """
    Loads nurse prompts from Excel.

    Workbook is loaded once and cached in memory.
    """

    MASTER_SHEET = "MASTER — All Prompts"

    def __init__(self, excel_path: str):

        self.excel_path = Path(excel_path)

        self.prompts: List[NursePrompt] = []

        self.prompt_lookup: Dict[str, NursePrompt] = {}

        self.load()

    ##############################################################

    def load(self):

        workbook = load_workbook(

            self.excel_path,

            data_only=True

        )

        sheet = workbook[self.MASTER_SHEET]

        rows = list(sheet.iter_rows(values_only=True))

        header_row = None

        for idx, row in enumerate(rows):

            if row and "Prompt ID" in row:

                header_row = idx

                break

        if header_row is None:

            raise RuntimeError(
                "Unable to locate Prompt ID header."
            )

        headers = [

            str(c).strip() if c else ""

            for c in rows[header_row]

        ]

        for row in rows[header_row + 1:]:

            if not any(row):
                continue

            values = dict(zip(headers, row))

            prompt = NursePrompt(

                prompt_id=str(
                    values.get("Prompt ID", "")
                ),

                job_aid=str(
                    values.get("Job Aid", "")
                ),

                category=str(
                    values.get("Category", "")
                ),

                severity_level=str(
                    values.get("Severity Level", "")
                ),

                evaluation_prompt=str(
                    values.get("Evaluation Prompt", "")
                ),

                document_source=str(
                    values.get("Document Source", "")
                ),

                expected_finding=str(
                    values.get("Expected Finding", "")
                ),

                red_flag=str(
                    values.get("Red Flag", "")
                ),

                guideline=str(
                    values.get("Guideline", "")
                ),

                decision_impact=str(
                    values.get("Decision Impact", "")
                ),

                rag_search_keywords=str(
                    values.get("RAG Search Keywords", "")
                ),

                sheet_name=self.MASTER_SHEET,

            )

            self.prompts.append(prompt)

            self.prompt_lookup[prompt.prompt_id] = prompt

    ##############################################################

    def get_all(self):

        return self.prompts

    ##############################################################

    def get_prompt(

        self,

        prompt_id: str,

    ):

        return self.prompt_lookup.get(prompt_id)

    ##############################################################

    def get_job_aids(self):

        return sorted(

            {

                p.job_aid

                for p in self.prompts

            }

        )

    ##############################################################

    def get_categories(

        self,

        job_aid=None,

    ):

        prompts = self.prompts

        if job_aid:

            prompts = [

                p

                for p in prompts

                if p.job_aid == job_aid

            ]

        return sorted(

            {

                p.category

                for p in prompts

            }

        )

    ##############################################################

    def get_by_job_aid(

        self,

        job_aid,

    ):

        return [

            p

            for p in self.prompts

            if p.job_aid == job_aid

        ]

    ##############################################################

    def search(

        self,

        keyword,

    ):

        keyword = keyword.lower()

        return [

            p

            for p in self.prompts

            if keyword in p.evaluation_prompt.lower()

        ]