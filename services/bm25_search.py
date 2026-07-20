from rank_bm25 import BM25Okapi


class BM25Search:

    def __init__(self, collection):

        print("Loading BM25 Index...")

        results = collection.get(
            include=[
                "documents",
                "metadatas"
            ]
        )

        self.documents = results["documents"]
        self.metadatas = results["metadatas"]

        self.tokenized_documents = [
            doc.lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

        print("BM25 Ready.")

    def search(
        self,
        question,
        equipment_tag=None,
        top_k=20
    ):

        query = question.lower().split()

        scores = self.bm25.get_scores(query)

        ranked = sorted(

            zip(
                scores,
                self.documents,
                self.metadatas
            ),

            key=lambda x: x[0],

            reverse=True

        )

        output = []

        for score, doc, meta in ranked:

            if equipment_tag:

                if meta.get(
                    "equipment_tag"
                ) != equipment_tag.upper():

                    continue

            output.append(

                {

                    "document": doc,

                    "metadata": meta,

                    "score": float(score),

                    "source": "bm25"

                }

            )

            if len(output) >= top_k:

                break

        return output