from backend.prompts.summary_prompt import SUMMARY_PROMPT


prompt = SUMMARY_PROMPT.invoke(

    {

        "context": """

Patient

John Doe

Diagnosis

Pneumonia

Treatment

IV Antibiotics

Discharged after 4 days.

""",

        "question":"Generate summary"

    }

)

print(prompt.messages[0].content)

print("="*60)

print(prompt.messages[1].content)