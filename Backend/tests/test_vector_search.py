from Backend.app.services.retriever import Retriever

r=Retriever()

docs=r.retrieve(

    "Does patient have COVID-19?",

    "COVID-19"

)

for d in docs:

    print(d)