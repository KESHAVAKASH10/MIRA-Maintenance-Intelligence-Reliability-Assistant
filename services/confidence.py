class ConfidenceCalculator:

    def __init__(self):
        pass

    def calculate(

        self,

        documents

    ):

        if len(documents) == 0:

            return 0

        scores = []

        for doc in documents:

            if "rerank_score" in doc:

                scores.append(

                    doc["rerank_score"]

                )

            elif doc["source"] == "vector":

                scores.append(

                    max(

                        0,

                        1 - doc["score"]

                    )

                )

            else:

                scores.append(

                    min(

                        1,

                        doc["score"] / 20

                    )

                )

        confidence = (

            sum(scores)

            / len(scores)

        ) * 100

        confidence = round(confidence)

        confidence = max(

            0,

            min(

                100,

                confidence

            )

        )

        return confidence

    def label(

        self,

        confidence

    ):

        if confidence >= 85:

            return "Very High"

        elif confidence >= 70:

            return "High"

        elif confidence >= 50:

            return "Medium"

        elif confidence >= 30:

            return "Low"

        else:

            return "Very Low"