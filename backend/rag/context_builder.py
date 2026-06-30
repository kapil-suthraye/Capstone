class ContextBuilder:

    def build(

        self,

        documents

    ):

        context = []

        for i, doc in enumerate(

            documents,

            start=1

        ):

            page = doc.metadata.get(

                "page"

            )

            source = doc.metadata.get(

                "source"

            )

            context.append(

f"""
==========================

Document {i}

Source : {source}

Page : {page}

--------------------------

{doc.page_content}

"""

            )

        return "\n".join(context)