from fastapi import APIRouter

from Backend.app.db.review_store import review_store

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"]
)

@router.get("/dashboard")
async def dashboard():

    return review_store.list_dashboard_claims()