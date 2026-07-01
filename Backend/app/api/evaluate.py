from fastapi import APIRouter

from Backend.app.models.api_models import EvaluateRequest
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
):

    prompt = loader.get_prompt(
        request.prompt_id
    )

    if prompt is None:

        return {

            "error": "Prompt not found"

        }

    result = await llm.evaluate(

        namespace=request.namespace,

        prompt=prompt,

    )

    return result