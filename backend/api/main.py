from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(

    title="Medical AI Reviewer",

    version="1.0",

    description="Medical Claim Review API"

)

app.include_router(router)


@app.get("/")
def health():

    return {

        "status": "running",

        "application": "Medical AI Reviewer"

    }