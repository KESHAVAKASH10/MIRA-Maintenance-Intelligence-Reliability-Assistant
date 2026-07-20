import chromadb
from sentence_transformers import SentenceTransformer


class VectorSearch:

    def __init__(self):

        print("Loading Vector Search...")

        self.embedder = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_collection(
            "axis_knowledge"
        )

        print("Vector Search Ready.")

    def search(
        self,
        question,
        equipment_tag=None,
        top_k=20
    ):

        embedding = self.embedder.encode(
            question
        ).tolist()

        if equipment_tag:

            results = self.collection.query(
                query_embeddings=[embedding],
                where={
                    "equipment_tag": equipment_tag.upper()
                },
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

        else:

            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        output = []

        for doc, meta, dist in zip(
            docs,
            metas,
            distances
        ):

            output.append(
                {
                    "document": doc,
                    "metadata": meta,
                    "score": float(dist),
                    "source": "vector"
                }
            )

        return output