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

    supporting_evidence: List[str]

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
        You are an expert clinical documentation reviewer.

        Answer ONLY using the supplied clinical context.

        If the answer is not supported,
        respond exactly:

        Answer: Insufficient Evidence

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
            diagnosis_tag=prompt.job_aid,
        )

        context, evidence = self.build_context(docs)

        messages = self.PROMPT.format_messages(

            question=prompt.evaluation_prompt,

            context=context,

        )

        response = await self.llm.ainvoke(messages)

        data = json.loads(response.content)

        return EvaluationResult(

            answer=data["answer"],

            justification=data["justification"],

            supporting_evidence=evidence,

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