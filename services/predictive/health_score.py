import re


class HealthScore:

    def __init__(self):
        pass

    def calculate(self, documents):

        score = 100

        work_orders = 0
        incidents = 0
        inspections = 0

        vibration = []
        temperature = []

        for item in documents:

            meta = item["metadata"]
            text = item["document"].lower()

            doc_type = meta.get("doc_type", "")

            if doc_type == "work_order":
                work_orders += 1

            elif doc_type == "incident_report":
                incidents += 1

            elif doc_type == "inspection_record":
                inspections += 1

            vibration_matches = re.findall(
                r"(\d+\.?\d*)\s*mm/s",
                text
            )

            for value in vibration_matches:
                try:
                    vibration.append(float(value))
                except:
                    pass

            temp_matches = re.findall(
                r"(\d+\.?\d*)\s*°?c",
                text
            )

            for value in temp_matches:
                try:
                    temperature.append(float(value))
                except:
                    pass

            if "lubrication overdue" in text:
                score -= 8

            if "bearing failure" in text:
                score -= 20

            if "seal failure" in text:
                score -= 12

            if "trip" in text:
                score -= 10

            if "near miss" in text:
                score -= 6

        score -= work_orders * 2
        score -= incidents * 8

        if len(vibration):

            avg_vibration = sum(vibration) / len(vibration)

            if avg_vibration > 6:
                score -= 20

            elif avg_vibration > 4:
                score -= 10

        if len(temperature):

            avg_temp = sum(temperature) / len(temperature)

            if avg_temp > 90:
                score -= 15

            elif avg_temp > 75:
                score -= 8

        score = max(0, min(100, score))

        return {

            "health_score": round(score, 1),

            "statistics": {

                "work_orders": work_orders,

                "incidents": incidents,

                "inspections": inspections,

                "average_vibration": round(
                    sum(vibration) / len(vibration),
                    2
                ) if vibration else None,

                "average_temperature": round(
                    sum(temperature) / len(temperature),
                    2
                ) if temperature else None

            }

        }