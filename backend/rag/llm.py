from langchain_openai import ChatOpenAI

from backend.config import OPENAI_API_KEY


class MedicalLLM:

    def __init__(self):

        self.llm = ChatOpenAI(

            api_key=OPENAI_API_KEY,

            model="gpt-4o",

            temperature=0

        )

    def get_llm(self):

        return self.llm