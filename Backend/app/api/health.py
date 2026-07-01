from fastapi import APIRouter

from Backend.app.models.api_models import HealthResponse

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return HealthResponse(

        status="Healthy",

        version="1.0.0"

    )