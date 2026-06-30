import pandas as pd


class PromptBuilder:
    """
    Builds a structured prompt by combining:
    1. Retrieved medical evidence
    2. Disease-specific guideline worksheet
    """

    def build(
        self,
        diagnosis: str,
        medical_context: str,
        guideline_df: pd.DataFrame
    ):

        guideline_text = self._format_guideline(
            guideline_df
        )

        prompt = f"""
====================================================
MEDICAL AI REVIEWER
====================================================

PRIMARY DIAGNOSIS

{diagnosis}

----------------------------------------------------

PATIENT MEDICAL EVIDENCE

----------------------------------------------------

{medical_context}

----------------------------------------------------

CLINICAL REVIEW GUIDELINE

----------------------------------------------------

{guideline_text}

----------------------------------------------------

TASK

----------------------------------------------------

You are an experienced Clinical Nurse Reviewer.

Review ONLY the supplied medical evidence.

Compare the patient documentation with the
clinical review guideline.

Generate a review in the following JSON format.

{{
  "diagnosis": "",
  "summary": "",
  "evidence": [
    {{
      "finding": "",
      "source": "",
      "page": 0
    }}
  ],
  "missing_documentation": [],
  "recommendation": "",
  "confidence": 0.0
}}

Rules:

1. Return ONLY JSON.
2. Do NOT use markdown.
3. Do NOT wrap JSON inside ``` blocks.
4. If information is unavailable, use "Not Available".
5. Evidence must always include source PDF and page number.
"""

        return prompt

    def _format_guideline(
        self,
        guideline_df
    ):

        lines = []

        guideline_df = guideline_df.fillna("")

        for _, row in guideline_df.iterrows():

            for column in guideline_df.columns:

                value = str(row[column]).strip()

                if value:

                    lines.append(
                        f"{column}: {value}"
                    )

            lines.append("-" * 60)

        return "\n".join(lines)