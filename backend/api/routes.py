from fastapi import APIRouter, HTTPException

from backend.models.review_request import ReviewRequest
from backend.rag.review_engine import ReviewEngine

router = APIRouter()

engine = ReviewEngine()


@router.post("/review")
def review_claim(request: ReviewRequest):

    try:

        review = engine.review(request)

        return review.model_dump()

    except Exception as ex:

        raise HTTPException(

            status_code=500,

            detail=str(ex)

        )