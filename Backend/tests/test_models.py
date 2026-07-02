from openai import OpenAI
from Backend.app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

models = client.models.list()

for m in models.data:
    print(m.id)