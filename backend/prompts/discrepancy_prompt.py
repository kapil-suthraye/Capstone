from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.system_prompts import (
    MEDICAL_SYSTEM_PROMPT
)

DISCREPANCY_PROMPT = ChatPromptTemplate.from_messages(

    [

        ("system", MEDICAL_SYSTEM_PROMPT),

        (

            "human",

            """
Medical Context

{context}

Question

{question}

Identify any inconsistencies between
medical documentation and claim information.

Return only supported discrepancies.

Do not speculate.
"""

        )

    ]

)