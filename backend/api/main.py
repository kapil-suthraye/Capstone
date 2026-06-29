from fastapi import FastAPI

app = FastAPI(

    title="Medical AI Reviewer",

    description="Enterprise Medical Claim Review API",

    version="1.0.0"

)


@app.get("/")
def health():

    return {

        "status": "running",

        "application": "Medical AI Reviewer",

        "version": "1.0.0"

    }