from services.context_builder import ContextBuilder


class ChatService:

    def __init__(

        self,

        knowledge_engine,

        llm

    ):

        self.engine = knowledge_engine

        self.llm = llm

        self.builder = ContextBuilder()

    def ask(

        self,

        question,

        equipment_tag=None

    ):

        result = self.engine.chat_search(

            question,

            equipment_tag

        )

        documents = result["documents"]

        context = result["context"]

        confidence = result["confidence"]

        confidence_label = result["confidence_label"]

        graph = result.get(

            "graph",

            {}

        )

        if len(documents) == 0:

            return {

                "answer": "I don't have enough information in the knowledge base to answer this question.",

                "confidence": confidence,

                "confidence_label": confidence_label,

                "sources": [],

                "graph": {},

                "equipment_tag": equipment_tag

            }

        prompt = self.builder.build_chat_prompt(

            question,

            context

        )

        response = self.llm.chat.completions.create(

            model="meta/llama-3.1-70b-instruct",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0.1,

            max_tokens=700

        )

        sources = []

        seen = set()

        for doc in documents:

            meta = doc["metadata"]

            key = (

                meta["filename"],

                meta["page_number"]

            )

            if key in seen:

                continue

            seen.add(key)

            sources.append(

                {

                    "filename": meta["filename"],

                    "page": meta["page_number"],

                    "equipment": meta.get(

                        "equipment_tag",

                        "GENERAL"

                    )

                }

            )

        related_assets = set()

        for doc in documents:

            equipment = doc["metadata"].get(

                "equipment_tag"

            )

            if equipment:

                related_assets.add(

                    equipment

                )

        return {

            "answer": response.choices[0].message.content,

            "confidence": confidence,

            "confidence_label": confidence_label,

            "sources": sources,

            "graph": graph,

            "related_assets": sorted(

                list(

                    related_assets

                )

            ),

            "equipment_tag": equipment_tag

        }