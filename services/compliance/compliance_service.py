from services.knowledge_engine import KnowledgeEngine


class ComplianceService:

    def __init__(self, knowledge_engine):

        self.engine = knowledge_engine

    def check(self, equipment_tag):

        result = self.engine.search(

            f"{equipment_tag} OISD Factories Act audit inspection work order incident compliance",

            equipment_tag=equipment_tag,

            top_k=20

        )

        docs = result["documents"]

        regulations = set()

        findings = set()

        work_orders = 0

        inspections = 0

        incidents = 0

        audits = 0

        for doc in docs:

            meta = doc["metadata"]

            filename = meta.get("filename", "")

            lower = filename.lower()

            page = meta.get("page_number", "")

            if "oisd" in lower:

                regulations.add(

                    filename.replace(".pdf", "")

                )

            if "factories" in lower:

                regulations.add(

                    "Factories Act 1948"

                )

            if "audit" in lower:

                audits += 1

                findings.add(

                    f"Compliance audit available ({filename})"

                )

            if "inspection" in lower:

                inspections += 1

                findings.add(

                    f"Inspection record found ({filename})"

                )

            if "incident" in lower or "near_miss" in lower:

                incidents += 1

                findings.add(

                    f"Incident history available ({filename})"

                )

            if "work_order" in lower or lower.startswith("wo_"):

                work_orders += 1

                findings.add(

                    f"Maintenance work order ({filename})"

                )

        score = 100

        score -= incidents * 10

        score -= max(0, work_orders - inspections) * 5

        score = max(0, min(score, 100))

        if score >= 90:

            status = "Excellent"

        elif score >= 75:

            status = "Compliant"

        elif score >= 60:

            status = "Needs Attention"

        else:

            status = "Critical"

        return {

            "equipment": equipment_tag,

            "compliance_score": score,

            "status": status,

            "confidence": result["confidence"],

            "regulations": sorted(list(regulations)),

            "findings": sorted(list(findings)),

            "statistics": {

                "audits": audits,

                "inspections": inspections,

                "incidents": incidents,

                "work_orders": work_orders

            }

        }