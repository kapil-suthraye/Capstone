from pydantic import BaseModel
from typing import List

class Evidence(BaseModel):

    page:int

    section:str

    quote:str

    chunk_id:str

class EvaluationResult(BaseModel):

    prompt_id:str

    answer:str

    justification:str

    confidence:float

    supporting_evidence:List[Evidence]