class EquipmentIndex:

    def __init__(self, knowledge_engine):

        self.engine = knowledge_engine

    def get_documents(

        self,

        equipment_tag,

        limit=10

    ):

        return self.engine.hybrid_search(

            equipment_tag,

            equipment_tag=equipment_tag,

            top_k=limit

        )