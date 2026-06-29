from backend.knowledge.guideline_loader import (
    GuidelineLoader
)

loader = GuidelineLoader()

tests = [

    "COVID",

    "Sepsis",

    "Pneumonia",

    "CHF",

    "Stroke"

]

for diagnosis in tests:

    print("=" * 70)

    print("Diagnosis :", diagnosis)

    df = loader.load(diagnosis)

    print(df.head(3))