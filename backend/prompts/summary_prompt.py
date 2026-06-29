from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.system_prompts import (
    MEDICAL_SYSTEM_PROMPT
)


SUMMARY_PROMPT = ChatPromptTemplate.from_messages(

    [

        (
            "system",

            MEDICAL_SYSTEM_PROMPT

        ),

        (

            "human",

            """
Medical Context

-------------------------

{context}

-------------------------

Question

{question}

Generate a concise clinical summary.

Include:

- Patient
- Diagnosis
- Treatment
- Admission
- Discharge
- Supporting evidence

If information is unavailable, mention it.
"""

        )

    ]

)