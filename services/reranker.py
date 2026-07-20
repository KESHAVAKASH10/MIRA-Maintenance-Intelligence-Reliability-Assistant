from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("Loading CrossEncoder...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("CrossEncoder Ready.")

    def rerank(

        self,

        question,

        documents,

        top_k=10

    ):

        if len(documents) == 0:

            return []

        pairs = [

            (

                question,

                doc["document"]

            )

            for doc in documents

        ]

        scores = self.model.predict(

            pairs

        )

        ranked = sorted(

            zip(

                scores,

                documents

            ),

            key=lambda x: x[0],

            reverse=True

        )

        output = []

        for score, doc in ranked[:top_k]:

            doc["rerank_score"] = float(score)

            output.append(doc)

        return output