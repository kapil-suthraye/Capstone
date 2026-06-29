from backend.knowledge.guideline_loader import (
    GuidelineLoader
)

from backend.knowledge.prompt_builder import (
    PromptBuilder
)

loader = GuidelineLoader()

df = loader.load("COVID")

medical_context = """
Patient Name : John Doe

Diagnosis : COVID-19

Temperature : 102 F

Oxygen Saturation : 89%

Chest CT

Ground Glass Opacity

Received Remdesivir
"""

builder = PromptBuilder()

prompt = builder.build(

    diagnosis="COVID",

    medical_context=medical_context,

    guideline_df=df

)

print(prompt)