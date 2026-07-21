from pathlib import Path
import chromadb


class DocumentService:

    def __init__(self):

        client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = client.get_collection(
            "axis_knowledge"
        )

    def get_all_documents(self):

        results = self.collection.get(
            include=["metadatas"]
        )

        documents = {}

        for meta in results["metadatas"]:

            filename = meta["filename"]

            if filename not in documents:

                documents[filename] = {

                    "filename": filename,

                    "doc_type": meta.get(
                        "doc_type",
                        "General"
                    ),

                    "equipment_tag": meta.get(
                        "equipment_tag",
                        "GENERAL"
                    ),

                    "pages": set(),

                    "chunks": 0

                }

            documents[filename]["pages"].add(
                meta["page_number"]
            )

            documents[filename]["chunks"] += 1

        output = []

        for doc in documents.values():

            doc["pages"] = len(
                doc["pages"]
            )

            output.append(doc)

        output.sort(
            key=lambda x: x["filename"]
        )

        return output

    def get_document(self, filename):

        results = self.collection.get(
            where={
                "filename": filename
            },
            include=[
                "documents",
                "metadatas"
            ]
        )

        if len(results["documents"]) == 0:

            return None

        return {

            "filename": filename,

            "chunks": results["documents"],

            "metadata": results["metadatas"]

        }

    def search(self, query):

        docs = self.get_all_documents()

        query = query.lower()

        return [

            d

            for d in docs

            if query in d["filename"].lower()

            or query in d["equipment_tag"].lower()

            or query in d["doc_type"].lower()

        ]