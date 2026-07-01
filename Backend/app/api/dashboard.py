from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"]
)


@router.get("/dashboard")
async def dashboard():

    return [

        {
            "claim_id": "CLM-1001",
            "patient": "John Smith",
            "diagnosis": "CHF",
            "status": "Completed",
            "review_date": "2026-07-01"
        },

        {
            "claim_id": "CLM-1002",
            "patient": "Mary Brown",
            "diagnosis": "Stroke",
            "status": "Pending",
            "review_date": "2026-07-01"
        }

    ]