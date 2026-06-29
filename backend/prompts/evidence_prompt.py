from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.system_prompts import (
    MEDICAL_SYSTEM_PROMPT
)

EVIDENCE_PROMPT = ChatPromptTemplate.from_messages(

    [

        ("system", MEDICAL_SYSTEM_PROMPT),

        (

            "human",

            """
Medical Context

{context}

Question

{question}

Return:

1. Evidence
2. Page reference
3. Explanation
4. Confidence
"""

        )

    ]

)