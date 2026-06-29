from langchain_core.output_parsers import StrOutputParser

from backend.rag.retriever import MedicalRetriever
from backend.rag.llm import MedicalLLM
from backend.rag.formatter import ContextFormatter

from backend.prompts.summary_prompt import SUMMARY_PROMPT


class MedicalRAG:

    def __init__(self):

        print("Initializing Medical RAG...")

        self.retriever = MedicalRetriever()

        self.llm = MedicalLLM().get_llm()

        self.parser = StrOutputParser()

    def ask(self, question):

        print("Searching Medical Documents...")

        docs = self.retriever.search(

            question,

            with_score=True

        )

        print(f"Retrieved {len(docs)} chunks.")

        context = ContextFormatter.format(docs)

        prompt = SUMMARY_PROMPT.invoke(

            {

                "context": context,

                "question": question

            }

        )

        response = self.llm.invoke(

            prompt.messages

        )

        answer = self.parser.invoke(

            response

        )

        return {

            "answer": answer,

            "context": context,

            "documents": docs

        }