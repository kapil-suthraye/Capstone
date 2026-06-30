from pydantic import BaseModel


class ReviewRequest(BaseModel):

    claim_id: str

    pdf_name: str