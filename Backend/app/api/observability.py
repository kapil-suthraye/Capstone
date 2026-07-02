from fastapi import APIRouter

from Backend.app.core.metrics import metrics
from Backend.app.db.review_store import review_store

router = APIRouter(
    prefix="/api",
    tags=["Observability"],
)


@router.get("/metrics")
async def metrics_snapshot():
    return metrics.snapshot()


@router.get("/observability")
async def observability_snapshot():
    return {
        "system": metrics.snapshot(),
        "ragas": review_store.ragas_snapshot(),
        "claims": review_store.list_dashboard_claims(),
    }