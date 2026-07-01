from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.app.api.health import router as health_router
from Backend.app.api.prompts import router as prompts_router
from Backend.app.api.upload import router as upload_router
from Backend.app.api.evaluate import router as evaluate_router

from Backend.app.api.dashboard import router as dashboard_router



app = FastAPI(
    title="Medical AI Reviewer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(prompts_router)
app.include_router(upload_router)
app.include_router(evaluate_router)
app.include_router(dashboard_router)