from pydantic import BaseModel


class EvaluationRequest(BaseModel):

    namespace: str

    prompt_id: str