import networkx as nx


class GraphQuery:

    def __init__(self, graph):

        self.graph = graph

    def equipment_exists(

        self,

        equipment_tag

    ):

        node = f"EQUIPMENT::{equipment_tag.upper()}"

        return node in self.graph

    def get_equipment(

        self,

        equipment_tag

    ):

        node = f"EQUIPMENT::{equipment_tag.upper()}"

        if node not in self.graph:

            return None

        return self.graph.nodes[node]

    def get_neighbors(

        self,

        equipment_tag

    ):

        node = f"EQUIPMENT::{equipment_tag.upper()}"

        if node not in self.graph:

            return []

        neighbors = []

        for neighbor in self.graph.neighbors(node):

            edge = self.graph.edges[node, neighbor]

            neighbors.append({

                "id": neighbor,

                "relation": edge["relation"],

                "data": self.graph.nodes[neighbor]

            })

        return neighbors

    def get_documents(

        self,

        equipment_tag

    ):

        node = f"EQUIPMENT::{equipment_tag.upper()}"

        if node not in self.graph:

            return []

        documents = []

        for neighbor in self.graph.neighbors(node):

            edge = self.graph.edges[node, neighbor]

            if edge["relation"] == "HAS_DOCUMENT":

                documents.append({

                    "id": neighbor,

                    **self.graph.nodes[neighbor]

                })

        return documents

    def get_related_nodes(

        self,

        equipment_tag,

        relation

    ):

        node = f"EQUIPMENT::{equipment_tag.upper()}"

        if node not in self.graph:

            return []

        output = []

        for neighbor in self.graph.neighbors(node):

            edge = self.graph.edges[node, neighbor]

            if edge["relation"] == relation:

                output.append({

                    "id": neighbor,

                    **self.graph.nodes[neighbor]

                })

        return output

    def shortest_path(

        self,

        source,

        target

    ):

        source_node = f"EQUIPMENT::{source.upper()}"

        target_node = f"EQUIPMENT::{target.upper()}"

        try:

            return nx.shortest_path(

                self.graph,

                source_node,

                target_node

            )

        except Exception:

            return []

    def statistics(self):

        return {

            "nodes": self.graph.number_of_nodes(),

            "edges": self.graph.number_of_edges(),

            "connected_components": nx.number_weakly_connected_components(

                self.graph

            )

        }