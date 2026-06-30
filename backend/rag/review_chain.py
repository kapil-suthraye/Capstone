import json

from langchain_core.messages import HumanMessage

from backend.rag.medical_retriever import (
    MedicalRetriever
)

from backend.rag.diagnosis_detector import (
    DiagnosisDetector
)

from backend.rag.context_builder import (
    ContextBuilder
)

from backend.knowledge.guideline_loader import (
    GuidelineLoader
)

from backend.knowledge.prompt_builder import (
    PromptBuilder
)

from backend.rag.llm import (
    MedicalLLM
)


class MedicalReviewChain:

    def __init__(self):

        self.retriever = MedicalRetriever()

        self.detector = DiagnosisDetector()

        self.context_builder = ContextBuilder()

        self.guidelines = GuidelineLoader()

        self.prompt_builder = PromptBuilder()

        self.llm = MedicalLLM().get_llm()

    def review(

        self,

        question

    ):

        print()

        print("Searching Medical Records...")

        docs = self.retriever.search(

            question

        )

        print("Detecting Diagnosis...")

        diagnosis = self.detector.detect(

            docs

        )

        print(

            f"Diagnosis: {diagnosis}"

        )

        print("Loading Guidelines...")

        guideline = self.guidelines.load(

            diagnosis

        )

        medical_context = self.context_builder.build(

            docs

        )

        prompt = self.prompt_builder.build(

            diagnosis,

            medical_context,

            guideline

        )

        response = self.llm.invoke(

            [

                HumanMessage(

                    content=prompt

                )

            ]

        )

        return response.content