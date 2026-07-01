from fastapi import APIRouter, HTTPException

from Backend.app.db.review_store import review_store
from Backend.app.models.claim_summary import ClaimSummary

router = APIRouter(
    prefix="/api",
    tags=["Claim Summary"],
)


@router.get(
    "/claims/{namespace}/summary",
    response_model=ClaimSummary,
)
async def claim_summary(namespace: str) -> ClaimSummary:
    summary = review_store.build_summary(namespace)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Claim summary not found for namespace",
        )

    return summary