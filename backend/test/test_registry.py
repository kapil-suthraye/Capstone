from backend.knowledge.registry import KnowledgeRegistry

registry = KnowledgeRegistry()

tests = [

    "COVID",

    "Coronavirus",

    "Pneumonia",

    "CHF",

    "Stroke"

]

for diagnosis in tests:

    sheet = registry.get_sheet(
        diagnosis
    )

    print(f"{diagnosis} -> {sheet}")