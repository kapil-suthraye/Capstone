class ContextFormatter:

    @staticmethod
    def format(results):

        context = []

        for i, (doc, score) in enumerate(results, start=1):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "Unknown")

            chunk = f"""
==============================
Document {i}
==============================

Source : {source}
Page   : {page + 1 if isinstance(page, int) else page}
Similarity Score : {score:.4f}

Content:

{doc.page_content}

"""

            context.append(chunk)

        return "\n".join(context)