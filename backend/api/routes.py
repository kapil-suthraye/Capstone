from fastapi import APIRouter, HTTPException

from backend.models.review_request import ReviewRequest
from backend.rag.review_engine import ReviewEngine

router = APIRouter()

engine = ReviewEngine()

@router.post("/review")
def review_claim(request: ReviewRequest):

    """
    Executes the complete Medical AI Review pipeline.

    Flow

        Request
            ↓
        Retriever
            ↓
        Diagnosis Detection
            ↓
        Guideline Loading
            ↓
        Prompt Construction
            ↓
        GPT-4o Review
            ↓
        Structured ReviewResponse

    """

    try:

        review = engine.review(request)

        return review.model_dump()

    except FileNotFoundError as ex:

        raise HTTPException(

            status_code=404,

            detail=str(ex)

        )

    except ValueError as ex:

        raise HTTPException(

            status_code=400,

            detail=str(ex)

        )

    except Exception as ex:

        raise HTTPException(

            status_code=500,

            detail=f"Medical Review Failed : {str(ex)}"

        )