from fastapi import APIRouter

from .routers import upload
from .routers import evaluate
from .routers import prompts
from .routers import dashboard
from .routers import health

api_router=APIRouter()

api_router.include_router(upload.router)

api_router.include_router(evaluate.router)

api_router.include_router(prompts.router)

api_router.include_router(dashboard.router)

api_router.include_router(health.router)