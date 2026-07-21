from services.context_builder import ContextBuilder


class EquipmentService:

    def __init__(

        self,

        knowledge_engine,

        llm

    ):

        self.engine = knowledge_engine

        self.llm = llm

        self.builder = ContextBuilder()

    def get_equipment_report(

        self,

        equipment_tag

    ):

        result = self.engine.equipment_search(

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

                "equipment_tag": equipment_tag,

                "status": "not_found",

                "message": f"No information found for {equipment_tag}.",

                "intelligence_summary": "",

                "work_orders": [],

                "incidents": [],

                "inspections": [],

                "manuals": [],

                "regulations": [],

                "related_assets": [],

                "graph": {},

                "confidence": confidence,

                "confidence_label": confidence_label,

                "total_documents_found": 0

            }

        prompt = self.builder.build_equipment_prompt(

            equipment_tag,

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

            max_tokens=600

        )

        work_orders = []

        incidents = []

        inspections = []

        manuals = []

        regulations = []

        related_assets = set()

        for item in documents:

            meta = item["metadata"]

            entry = {

                "filename": meta["filename"],

                "page": meta["page_number"],

                "preview": item["document"][:200]

            }

            equipment = meta.get(

                "equipment_tag"

            )

            if equipment:

                related_assets.add(

                    equipment

                )

            doc_type = meta.get(

                "doc_type",

                "general_document"

            )

            if doc_type == "work_order":

                work_orders.append(entry)

            elif doc_type == "incident_report":

                incidents.append(entry)

            elif doc_type == "inspection_record":

                inspections.append(entry)

            elif doc_type == "equipment_manual":

                manuals.append(entry)

            elif doc_type == "regulatory_standard":

                regulations.append(entry)

        return {

            "equipment_tag": equipment_tag,

            "intelligence_summary": response.choices[0].message.content,

            "confidence": confidence,

            "confidence_label": confidence_label,

            "graph": graph,

            "related_assets": sorted(

                list(

                    related_assets

                )

            ),

            "work_orders": work_orders,

            "incidents": incidents,

            "inspections": inspections,

            "manuals": manuals,

            "regulations": regulations,

            "total_documents_found": len(documents)

        }