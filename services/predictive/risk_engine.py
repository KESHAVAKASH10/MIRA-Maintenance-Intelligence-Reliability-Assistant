class RiskEngine:

    def __init__(self):
        pass

    def evaluate(

        self,

        health_score,

        statistics

    ):

        risk_score = 100 - health_score

        incidents = statistics.get(

            "incidents",

            0

        )

        work_orders = statistics.get(

            "work_orders",

            0

        )

        vibration = statistics.get(

            "average_vibration"

        )

        temperature = statistics.get(

            "average_temperature"

        )

        if incidents >= 3:
            risk_score += 15

        elif incidents >= 1:
            risk_score += 8

        if work_orders >= 5:
            risk_score += 10

        elif work_orders >= 2:
            risk_score += 5

        if vibration:

            if vibration >= 6:
                risk_score += 15

            elif vibration >= 4:
                risk_score += 8

        if temperature:

            if temperature >= 90:
                risk_score += 15

            elif temperature >= 75:
                risk_score += 8

        risk_score = max(

            0,

            min(

                100,

                risk_score

            )

        )

        if risk_score >= 80:

            level = "Critical"

            color = "red"

        elif risk_score >= 60:

            level = "High"

            color = "orange"

        elif risk_score >= 35:

            level = "Medium"

            color = "yellow"

        else:

            level = "Low"

            color = "green"

        return {

            "risk_score": round(

                risk_score,

                1

            ),

            "risk_level": level,

            "color": color

        }