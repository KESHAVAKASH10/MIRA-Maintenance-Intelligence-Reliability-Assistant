from services.knowledge_engine import KnowledgeEngine

class ComplianceService:

    def __init__(self, knowledge_engine):

        self.engine = knowledge_engine

    def check(self, equipment_tag):

        result = self.engine.search(
            f"{equipment_tag} OISD Factories Act audit compliance checklist",
            equipment_tag=equipment_tag,
            top_k=12
        )

        documents = result["documents"]

        regulations = []

        findings = []

        for doc in documents:

            filename = doc["metadata"]["filename"]

            lower = filename.lower()

            if "oisd" in lower or "factories" in lower:

                regulations.append(filename)

            if "audit" in lower:

                findings.append(
                    "Audit report available."
                )

            if "inspection" in lower:

                findings.append(
                    "Inspection record available."
                )

        score = max(
            0,
            100 - (5 * max(0, 5 - len(findings)))
        )

        return {

            "equipment": equipment_tag,

            "compliance_score": score,

            "status":

                "Compliant"

                if score >= 80

                else

                "Needs Attention",

            "regulations": list(set(regulations)),

            "findings": findings,

            "confidence": result["confidence"]

        }