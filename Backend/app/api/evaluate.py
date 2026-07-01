from fastapi import APIRouter
from fastapi import HTTPException

from Backend.app.core.logging import logger
from Backend.app.models.api_models import EvaluateRequest
from Backend.app.models.evaluation_result import EvaluationResult
from Backend.app.db.review_store import review_store
from Backend.app.services.llm_service import LLMService
from Backend.app.services.nurse_prompts import NursePromptLoader
from Backend.app.core.config import settings

router = APIRouter(
    prefix="/api",
    tags=["Evaluation"]
)

loader = NursePromptLoader(
    settings.NURSE_PROMPTS_FILE
)

llm = LLMService()

@router.post("/evaluate")
async def evaluate(
    request: EvaluateRequest
) -> EvaluationResult:

    prompt = loader.get_prompt(
        request.prompt_id
    )

    if prompt is None:
        raise HTTPException(
            status_code=404,
            detail="Prompt not found",
        )

    result = await llm.evaluate(

        namespace=request.namespace,

        prompt=prompt,

    )

    review_store.add_evaluation(
        namespace=request.namespace,
        prompt=prompt,
        result=result,
    )

    logger.bind(
        namespace=request.namespace,
        prompt_id=request.prompt_id,
        verdict=result.verdict,
        confidence=result.confidence,
    ).info("evaluation_recorded")

    return result