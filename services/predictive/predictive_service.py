from services.predictive.health_score import HealthScore
from services.predictive.risk_engine import RiskEngine
from services.predictive.failure_predictor import FailurePredictor
from services.predictive.maintenance_recommender import MaintenanceRecommender


class PredictiveService:

    def __init__(self):

        self.health = HealthScore()

        self.risk = RiskEngine()

        self.failure = FailurePredictor()

        self.recommender = MaintenanceRecommender()

    def predict(

        self,

        documents

    ):

        health_result = self.health.calculate(

            documents

        )

        health_score = health_result["health_score"]

        statistics = health_result["statistics"]

        risk_result = self.risk.evaluate(

            health_score,

            statistics

        )

        prediction = self.failure.predict(

            health_score,

            risk_result["risk_score"],

            statistics

        )

        recommendation = self.recommender.recommend(

            health_score,

            risk_result["risk_level"],

            prediction,

            statistics

        )

        return {

            "health_score": health_score,

            "statistics": statistics,

            "risk_score": risk_result["risk_score"],

            "risk_level": risk_result["risk_level"],

            "risk_color": risk_result["color"],

            "failure_probability": prediction["failure_probability"],

            "remaining_useful_life_days": prediction["remaining_useful_life_days"],

            "maintenance_priority": prediction["maintenance_priority"],

            "recommendations": recommendation["recommendations"]

        }