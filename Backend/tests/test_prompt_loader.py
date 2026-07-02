from Backend.app.services.nurse_prompts import NursePromptLoader

from pathlib import Path

from Backend.app.core.config import settings

loader = NursePromptLoader(
    settings.NURSE_PROMPTS_FILE
)
print()

print("=" * 80)

print("Total Prompts")

print(len(loader.get_all()))

print()

print("=" * 80)

print("Job Aids")

print(loader.get_job_aids())

print()

print("=" * 80)

print("CHF")

for p in loader.get_by_job_aid("CHF-ADHF")[:5]:

    print()

    print(p.prompt_id)

    print(p.category)

    print(p.evaluation_prompt)

    print(p.rag_search_keywords)