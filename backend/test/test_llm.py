from langchain_core.messages import HumanMessage

from backend.rag.llm import MedicalLLM


print("=" * 60)
print("Medical AI Reviewer - GPT Test")
print("=" * 60)

llm = MedicalLLM().get_llm()

question = input("\nAsk GPT: ")

response = llm.invoke(

    [

        HumanMessage(

            content=question

        )

    ]

)

print()

print("=" * 60)
print("GPT Response")
print("=" * 60)

print(response.content)