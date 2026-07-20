import networkx as nx
import chromadb


class GraphBuilder:

    def __init__(self):

        self.graph = nx.DiGraph()

        client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = client.get_collection(
            "axis_knowledge"
        )

    def build(self):

        self.graph.clear()

        results = self.collection.get(
            include=["documents", "metadatas"]
        )

        documents = results["documents"]
        metadatas = results["metadatas"]

        for document, meta in zip(documents, metadatas):

            equipment = meta.get(
                "equipment_tag",
                "GENERAL"
            ).upper()

            filename = meta.get(
                "filename",
                "Unknown"
            )

            page = meta.get(
                "page_number",
                "-"
            )

            doc_type = meta.get(
                "doc_type",
                "general_document"
            )

            equipment_node = f"EQUIPMENT::{equipment}"

            document_node = (
                f"DOCUMENT::{filename}"
                f"::PAGE::{page}"
            )

            self.graph.add_node(

                equipment_node,

                label=equipment,

                node_type="equipment"

            )

            self.graph.add_node(

                document_node,

                label=filename,

                node_type="document",

                page=page,

                doc_type=doc_type,

                text=document

            )

            self.graph.add_edge(

                equipment_node,

                document_node,

                relation="HAS_DOCUMENT"

            )

            if doc_type != "general_document":

                type_node = f"{doc_type.upper()}::{filename}"

                self.graph.add_node(

                    type_node,

                    label=doc_type,

                    node_type=doc_type

                )

                self.graph.add_edge(

                    equipment_node,

                    type_node,

                    relation=f"HAS_{doc_type.upper()}"

                )

                self.graph.add_edge(

                    type_node,

                    document_node,

                    relation="REFERENCES"

                )

        return self.graph

    def save(self, path="data/knowledge_graph.gpickle"):

        nx.write_gpickle(

            self.graph,

            path

        )

    def load(self, path="data/knowledge_graph.gpickle"):

        self.graph = nx.read_gpickle(path)

        return self.graph

    def get_graph(self):

        return self.graph