from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.system_prompts import (
    MEDICAL_SYSTEM_PROMPT
)

RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages(

    [

        ("system", MEDICAL_SYSTEM_PROMPT),

        (

            "human",

            """
Medical Context

{context}

Question

{question}

Provide:

1. Recommendation
2. Reason
3. Risk
4. Confidence
5. Next Action
"""

        )

    ]

)