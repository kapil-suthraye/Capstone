from fastapi import FastAPI

app = FastAPI(

    title="Medical AI Reviewer",

    description="Backend API for Medical Claim Review",

    version="1.0"

)


@app.get("/")
def home():

    return {

        "status": "Backend Running",

        "message": "Medical AI Reviewer API"

    }