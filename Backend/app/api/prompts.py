from fastapi import APIRouter

from Backend.app.core.config import settings
from Backend.app.services.nurse_prompts import NursePromptLoader

router = APIRouter(
    prefix="/api",
    tags=["Prompts"]
)

loader = NursePromptLoader(
    settings.NURSE_PROMPTS_FILE
)


@router.get("/prompts")
async def get_prompts():

    return loader.get_all()