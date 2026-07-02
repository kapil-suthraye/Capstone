from pydantic import BaseModel

class UploadResponse(BaseModel):

    document_id:str

    filename:str

    pages:int

    chunks:int

    status:str