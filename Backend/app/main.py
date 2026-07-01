from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from Backend.app.api.dashboard import router as dashboard_router
from Backend.app.api.evaluate import router as evaluate_router
from Backend.app.api.health import router as health_router
from Backend.app.api.observability import router as observability_router
from Backend.app.api.prompts import router as prompts_router
from Backend.app.api.summary import router as summary_router
from Backend.app.api.upload import router as upload_router
from Backend.app.core.config import settings
from Backend.app.core.logging import logger
from Backend.app.core.metrics import metrics



app = FastAPI(
    title="Medical AI Reviewer",
    version="1.0.0",
)

cors_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_observability_middleware(
    request: Request,
    call_next,
):
    request_id = uuid4().hex[:12]
    started = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        latency_ms = round((perf_counter() - started) * 1000, 2)
        metrics.observe_request(
            method=request.method,
            path=request.url.path,
            status_code=500,
            latency_ms=latency_ms,
        )
        logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            latency_ms=latency_ms,
        ).exception("request_failed")
        raise

    latency_ms = round((perf_counter() - started) * 1000, 2)
    metrics.observe_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency_ms,
    )
    response.headers["x-request-id"] = request_id

    logger.bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency_ms,
    ).info("request_completed")

    return response


app.include_router(health_router)
app.include_router(prompts_router)
app.include_router(upload_router)
app.include_router(evaluate_router)
app.include_router(dashboard_router)
app.include_router(summary_router)
app.include_router(observability_router)
