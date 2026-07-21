class FailurePredictor:

    def __init__(self):
        pass

    def predict(

        self,

        health_score,

        risk_score,

        statistics

    ):

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

        probability = (

            risk_score * 0.55

            + incidents * 6

            + work_orders * 2

        )

        if vibration:

            probability += vibration * 2

        if temperature:

            probability += max(

                0,

                (temperature - 60) * 0.4

            )

        probability = max(

            0,

            min(

                100,

                probability

            )

        )

        if probability >= 90:

            rul = 7

            priority = "Immediate"

        elif probability >= 75:

            rul = 15

            priority = "Urgent"

        elif probability >= 60:

            rul = 30

            priority = "High"

        elif probability >= 40:

            rul = 60

            priority = "Medium"

        else:

            rul = 120

            priority = "Low"

        return {

            "failure_probability": round(

                probability,

                1

            ),

            "remaining_useful_life_days": rul,

            "maintenance_priority": priority

        }