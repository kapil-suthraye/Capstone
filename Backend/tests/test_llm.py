import asyncio

from Backend.app.services.llm_service import LLMService


async def main():

    llm = LLMService()

    result = await llm.evaluate(

        namespace="sample",

        question="Does the patient have acute congestive heart failure?",

        diagnosis="CHF",

    )

    print(result.model_dump())


asyncio.run(main())