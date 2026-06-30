import json

from langchain_core.messages import HumanMessage

from backend.models.review_request import ReviewRequest
from backend.models.review_response import (
    ReviewResponse,
    EvidenceItem
)

from backend.rag.medical_retriever import MedicalRetriever
from backend.rag.diagnosis_detector import DiagnosisDetector
from backend.rag.context_builder import ContextBuilder
from backend.rag.llm import MedicalLLM

from backend.knowledge.guideline_loader import GuidelineLoader
from backend.knowledge.prompt_builder import PromptBuilder


class ReviewEngine:

    """
    Main AI Engine responsible for complete
    medical claim review.
    """

    def __init__(self):

        self.retriever = MedicalRetriever()

        self.detector = DiagnosisDetector()

        self.context_builder = ContextBuilder()

        self.guideline_loader = GuidelineLoader()

        self.prompt_builder = PromptBuilder()

        self.llm = MedicalLLM().get_llm()

    def review(
        self,
        request: ReviewRequest
    ) -> ReviewResponse:

        print("=" * 60)
        print("Medical AI Review Started")
        print("=" * 60)

        #
        # Step 1
        #

        print("Retrieving medical evidence...")

        documents = self.retriever.search(

            query="medical review",

            pdf_name=request.pdf_name,

            k=8

        )

        #
        # Step 2
        #

        print("Detecting diagnosis...")

        diagnosis = self.detector.detect(
            documents
        )

        print(
            f"Diagnosis : {diagnosis}"
        )

        #
        # Step 3
        #

        print("Loading guideline...")

        guideline_df = self.guideline_loader.load(
            diagnosis
        )

        #
        # Step 4
        #

        medical_context = self.context_builder.build(
            documents
        )

        #
        # Step 5
        #

        prompt = self.prompt_builder.build(

            diagnosis,

            medical_context,

            guideline_df

        )

        #
        # Step 6
        #

        print("Calling GPT-4o...")

        response = self.llm.invoke(

            [

                HumanMessage(
                    content=prompt
                )

            ]

        )

        #
        # Step 7
        #

        review_json = json.loads(
            response.content
        )

        #
        # Step 8
        #

        evidence = []

        for item in review_json["evidence"]:

            evidence.append(

                EvidenceItem(

                    finding=item["finding"],

                    source=item["source"],

                    page=item["page"]

                )

            )

        #
        # Step 9
        #

        review = ReviewResponse(

            claim_id=request.claim_id,

            diagnosis=review_json["diagnosis"],

            summary=review_json["summary"],

            evidence=evidence,

            missing_documentation=review_json[
                "missing_documentation"
            ],

            recommendation=review_json[
                "recommendation"
            ],

            confidence=review_json[
                "confidence"
            ],

            processing_steps=[

                {

                    "step": "Retrieve Medical Records",

                    "status": "Completed"

                },

                {

                    "step": "Detect Diagnosis",

                    "status": "Completed"

                },

                {

                    "step": "Load Clinical Guideline",

                    "status": "Completed"

                },

                {

                    "step": "Build Medical Context",

                    "status": "Completed"

                },

                {

                    "step": "Generate AI Review",

                    "status": "Completed"

                }

            ],

            timeline=[

                {

                    "title": "Medical Review Started",

                    "description": "Retriever initialized",

                    "status": "Completed"

                },

                {

                    "title": "Diagnosis Detected",

                    "description": review_json["diagnosis"],

                    "status": "Completed"

                },

                {

                    "title": "Evidence Retrieved",

                    "description": f"{len(evidence)} supporting findings located",

                    "status": "Completed"

                },

                {

                    "title": "Recommendation Generated",

                    "description": review_json["recommendation"],

                    "status": "Completed"

                }

            ]

        )
        print("Medical Review Completed.")

        return review