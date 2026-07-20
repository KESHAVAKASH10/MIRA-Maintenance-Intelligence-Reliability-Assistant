from services.graph.graph_builder import GraphBuilder
from services.graph.graph_query import GraphQuery


class GraphService:

    def __init__(self):

        self.builder = GraphBuilder()

        self.graph = self.builder.build()

        self.query = GraphQuery(
            self.graph
        )

    def rebuild(self):

        self.graph = self.builder.build()

        self.query = GraphQuery(
            self.graph
        )

        return {

            "status": "success",

            "nodes": self.graph.number_of_nodes(),

            "edges": self.graph.number_of_edges()

        }

    def statistics(self):

        return self.query.statistics()

    def equipment_graph(

        self,

        equipment_tag

    ):

        return {

            "equipment": self.query.get_equipment(
                equipment_tag
            ),

            "documents": self.query.get_documents(
                equipment_tag
            ),

            "neighbors": self.query.get_neighbors(
                equipment_tag
            )

        }

    def related(

        self,

        equipment_tag,

        relation

    ):

        return self.query.get_related_nodes(

            equipment_tag,

            relation

        )

    def shortest_path(

        self,

        source,

        target

    ):

        return self.query.shortest_path(

            source,

            target

        )