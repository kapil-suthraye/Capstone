from fastapi import APIRouter, Depends, HTTPException

from Backend.app.core.dependencies import get_llm_service, get_nurse_prompt_loader
from Backend.app.core.logging import logger
from Backend.app.db.review_store import review_store
from Backend.app.models.api_models import EvaluateRequest
from Backend.app.models.evaluation_result import EvaluationResult
from Backend.app.services.llm_service import LLMService
from Backend.app.services.nurse_prompts import NursePromptLoader

router = APIRouter(
    prefix="/api",
    tags=["Evaluation"],
)


@router.post("/evaluate", response_model=EvaluationResult)
async def evaluate(
    request: EvaluateRequest,
    llm: LLMService = Depends(get_llm_service),
    loader: NursePromptLoader = Depends(get_nurse_prompt_loader),
) -> EvaluationResult:
    prompt = loader.get_prompt(request.prompt_id)

    if prompt is None:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt '{request.prompt_id}' not found",
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
