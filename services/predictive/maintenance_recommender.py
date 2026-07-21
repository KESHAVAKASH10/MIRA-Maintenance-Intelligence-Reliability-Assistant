class MaintenanceRecommender:

    def __init__(self):
        pass

    def recommend(

        self,

        health_score,

        risk_level,

        prediction,

        statistics

    ):

        recommendations = []

        vibration = statistics.get(

            "average_vibration"

        )

        temperature = statistics.get(

            "average_temperature"

        )

        incidents = statistics.get(

            "incidents",

            0

        )

        if health_score < 50:

            recommendations.append(
                "Perform complete equipment inspection immediately."
            )

        if risk_level == "Critical":

            recommendations.append(
                "Schedule emergency maintenance shutdown."
            )

        elif risk_level == "High":

            recommendations.append(
                "Prioritize maintenance within the next maintenance window."
            )

        if vibration:

            if vibration >= 6:

                recommendations.append(
                    "Investigate excessive vibration and check bearing alignment."
                )

            elif vibration >= 4:

                recommendations.append(
                    "Increase vibration monitoring frequency."
                )

        if temperature:

            if temperature >= 90:

                recommendations.append(
                    "Inspect bearing lubrication and cooling immediately."
                )

            elif temperature >= 75:

                recommendations.append(
                    "Monitor bearing temperature during every shift."
                )

        if incidents >= 2:

            recommendations.append(
                "Perform root cause analysis for recurring failures."
            )

        if prediction["remaining_useful_life_days"] <= 15:

            recommendations.append(
                "Prepare spare parts and maintenance resources."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Continue preventive maintenance schedule."
            )

        return {

            "recommendations": recommendations,

            "maintenance_priority": prediction["maintenance_priority"]

        }