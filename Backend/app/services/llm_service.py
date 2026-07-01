from __future__ import annotations

import json
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel

from Backend.app.core.config import settings
from Backend.app.models.nurse_prompt import NursePrompt
from Backend.app.models.retrieved_chunk import RetrievedChunk
from Backend.app.services.vector_store import VectorStore

class EvaluationResult(BaseModel):

    answer: str

    justification: str

    supporting_evidence: List[SupportingEvidence]

class SupportingEvidence(BaseModel):
    page: str
    heading: str
    score: float | None = None
    evidence: str

class LLMService:

    def __init__(self):

        self.vector = VectorStore()

        self.llm = ChatOpenAI(

            model=settings.OPENAI_MODEL,

            api_key=settings.OPENAI_API_KEY,

            temperature=0,

        )

    PROMPT = ChatPromptTemplate.from_template(
        """
       Carefully inspect every retrieved chunk.

        The answer may appear using different wording,
        medical abbreviations,
        or synonymous clinical terminology.

        Only return Insufficient Evidence
        after reviewing every chunk.

        If partial evidence exists,
        provide the closest supported answer
        and explain why.
        Return valid JSON.

        Question

        {question}

        Clinical Context

        {context}

        JSON format

        {{
            "answer":"...",
            "justification":"...",
            "supporting_evidence":[]
        }}
        """
        )
    
    def build_context(

    self,

        docs: List[RetrievedChunk],

    ):

        context = []

        evidence = []

        for index, doc in enumerate(docs, start=1):

            ref = f"Chunk-{index}"

            evidence.append(ref)

            context.append(

                f"""
    [{ref}]

    Heading:
    {doc.metadata.get("section_heading")}

    Pages:
    {doc.metadata.get("page_start")}-
    {doc.metadata.get("page_end")}

    {doc.text}
    """
            )

        return "\n\n".join(context), evidence
    
    async def evaluate(
        self,
        namespace: str,
        prompt: NursePrompt,
    ):

        docs = await self.vector.retrieve(
            query=prompt.rag_search_keywords
                or prompt.evaluation_prompt,
            namespace=namespace,
            diagnosis_tag=None,
        )

        # ===================== DEBUG START =====================

        print("\n" + "=" * 100)
        print("PROMPT ID :", prompt.prompt_id)
        print("QUESTION  :", prompt.evaluation_prompt)
        print("NAMESPACE :", namespace)
        print("TOTAL RETRIEVED CHUNKS :", len(docs))
        print("=" * 100)

        for i, doc in enumerate(docs, start=1):

            print(f"\n----- Chunk {i} -----")

            print("Heading :",
                doc.metadata.get("section_heading"))

            print("Pages :",
                f"{doc.metadata.get('page_start')} - {doc.metadata.get('page_end')}")

            print("Diagnosis Tag :",
                doc.metadata.get("diagnosis_tag"))

            print("\nText:\n")

            print(doc.text[:1000])

            print("-" * 100)

        print("=" * 100 + "\n")

        # ===================== DEBUG END =====================

        context, evidence = self.build_context(docs)

        messages = self.PROMPT.format_messages(
            question=prompt.evaluation_prompt,
            context=context,
        )

        response = await self.llm.ainvoke(messages)

        data = json.loads(response.content)

        supporting_evidence = []

        for doc in docs:
            supporting_evidence.append({
                "page": f"{doc.metadata.get('page_start', '-')}"
                        + (
                            f" - {doc.metadata.get('page_end')}"
                            if doc.metadata.get("page_end") != doc.metadata.get("page_start")
                            else ""
                        ),
                "heading": doc.metadata.get("section_heading", "Unknown"),
                "evidence": doc.text[:300]
            })

        return EvaluationResult(
            answer=data["answer"],
            justification=data["justification"],
            supporting_evidence=supporting_evidence,
        )
    
    async def evaluate_all(

        self,

        namespace,

        prompts,

    ):

        results = []

        for prompt in prompts:

            result = await self.evaluate(

                namespace,

                prompt,

            )

            results.append(

                {

                    "category": prompt["category"],

                    "question": prompt["question"],

                    "result": result,

                }

            )

        return results