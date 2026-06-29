from langchain_openai import ChatOpenAI

from backend.config import OPENAI_API_KEY


class MedicalLLM:

    def __init__(self):

        if not OPENAI_API_KEY:

            raise ValueError(
                "OPENAI_API_KEY not found in .env"
            )

        self.llm = ChatOpenAI(

            api_key=OPENAI_API_KEY,

            model="gpt-4o",

            temperature=0,

            max_tokens=1500

        )

    def get_llm(self):

        return self.llm