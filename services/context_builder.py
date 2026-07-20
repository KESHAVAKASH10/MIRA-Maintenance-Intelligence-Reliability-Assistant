class ContextBuilder:

    def __init__(self):
        pass

    def build_context(

        self,

        documents,

        max_documents=5

    ):

        if len(documents) == 0:

            return ""

        context = ""

        for doc in documents[:max_documents]:

            meta = doc["metadata"]

            filename = meta.get(
                "filename",
                "Unknown"
            )

            page = meta.get(
                "page_number",
                "-"
            )

            equipment = meta.get(
                "equipment_tag",
                "GENERAL"
            )

            context += (
                f"\n"
                f"=====================================\n"
                f"Source : {filename}\n"
                f"Page   : {page}\n"
                f"Asset  : {equipment}\n"
                f"=====================================\n"
                f"{doc['document']}\n\n"
            )

        return context

    def build_equipment_prompt(

        self,

        equipment_tag,

        context

    ):

        return f"""
You are MIRA (Maintenance Intelligence & Reliability Assistant).

You are generating an Equipment 360 Report.

Equipment:
{equipment_tag}

Use ONLY the supplied context.

If something is missing, clearly say it is unavailable.

Return the report in this format:

1. Current Health Status
2. Summary
3. Recent Issues
4. Maintenance Recommendations
5. Relevant Regulations

Context:

{context}
"""

    def build_chat_prompt(

        self,

        question,

        context

    ):

        return f"""
You are MIRA.

Answer ONLY using the supplied context.

If the answer cannot be found,
say you do not have sufficient information.

Always cite filenames whenever possible.

Context:

{context}

Question:

{question}
"""