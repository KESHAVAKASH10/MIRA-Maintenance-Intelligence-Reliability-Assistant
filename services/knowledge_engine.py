from services.vector_search import VectorSearch
from services.bm25_search import BM25Search
from services.reranker import Reranker
from services.context_builder import ContextBuilder
from services.confidence import ConfidenceCalculator
from services.graph.graph_service import GraphService

import chromadb


class KnowledgeEngine:

    def __init__(self):

        print("Loading Knowledge Engine...")

        self.vector = VectorSearch()

        client = chromadb.PersistentClient(
            path="data/chroma"
        )

        collection = client.get_collection(
            "axis_knowledge"
        )

        self.bm25 = BM25Search(
            collection
        )

        self.reranker = Reranker()

        self.context_builder = ContextBuilder()

        self.confidence = ConfidenceCalculator()

        self.graph = GraphService()

        print("Knowledge Engine Ready.")

    def search(

        self,

        question,

        equipment_tag=None,

        top_k=10

    ):

        vector_results = self.vector.search(

            question,

            equipment_tag,

            top_k * 2

        )

        bm25_results = self.bm25.search(

            question,

            equipment_tag,

            top_k * 2

        )

        merged = {}

        for result in vector_results + bm25_results:

            meta = result["metadata"]

            key = (

                meta["filename"],

                meta["page_number"],

                meta["chunk_index"]

            )

            if key not in merged:

                merged[key] = result

                continue

            if result["source"] == "vector":

                merged[key]["vector_score"] = result["score"]

            else:

                merged[key]["bm25_score"] = result["score"]

        documents = list(

            merged.values()

        )

        documents = self.reranker.rerank(

            question,

            documents,

            top_k

        )

        confidence = self.confidence.calculate(

            documents

        )

        confidence_label = self.confidence.label(

            confidence

        )

        context = self.context_builder.build_context(

            documents

        )

        graph_information = {}

        if equipment_tag:

            graph_information = self.graph.equipment_graph(

                equipment_tag

            )

        return {

            "documents": documents,

            "context": context,

            "confidence": confidence,

            "confidence_label": confidence_label,

            "graph": graph_information

        }

    def equipment_search(

        self,

        equipment_tag

    ):

        return self.search(

            question=f"{equipment_tag} maintenance history inspection failure",

            equipment_tag=equipment_tag,

            top_k=10

        )

    def chat_search(

        self,

        question,

        equipment_tag=None

    ):

        return self.search(

            question=question,

            equipment_tag=equipment_tag,

            top_k=8

        )

    def graph_statistics(

        self

    ):

        return self.graph.statistics()

    def rebuild_graph(

        self

    ):

        return self.graph.rebuild()

    def equipment_graph(

        self,

        equipment_tag

    ):

        return self.graph.equipment_graph(

            equipment_tag

        )

    def get_equipment_graph(

        self,

        equipment_tag

    ):

        return self.graph.equipment_graph(

            equipment_tag

        )

    def shortest_path(

        self,

        source,

        target

    ):

        return self.graph.shortest_path(

            source,

            target

        )
