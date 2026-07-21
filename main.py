import os
from pathlib import Path
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

from services.knowledge_engine import KnowledgeEngine
from services.chat_service import ChatService
from services.equipment_service import EquipmentService
from services.graph.graph_service import GraphService
from services.predictive.predictive_service import PredictiveService
from services.document_service import DocumentService


load_dotenv()

print("Loading MIRA Backend...")

app = FastAPI(
    title="MIRA API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

llm = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

knowledge_engine = KnowledgeEngine()

predictive_service = PredictiveService()

graph_service = GraphService()

chat_service = ChatService(
    knowledge_engine,
    llm
)

equipment_service = EquipmentService(
    knowledge_engine,
    llm
)

document_service = DocumentService()

print("MIRA Backend Ready.")


class QuestionRequest(BaseModel):

    question: str

    equipment_tag: str | None = None


class GraphPathRequest(BaseModel):

    source: str

    target: str


@app.get("/")
def root():

    return {

        "status": "MIRA is running",

        "version": "2.0.0"

    }


@app.get("/health")
def health():

    documents = list(

        Path("documents").glob("*.pdf")

    )

    return {

        "status": "healthy",

        "chunks_indexed":
        knowledge_engine.vector.collection.count(),

        "documents":
        len(documents),

        "graph_nodes":
        knowledge_engine.graph_statistics()["nodes"],

        "graph_edges":
        knowledge_engine.graph_statistics()["edges"],

        "embedding_model":
        "BAAI/bge-small-en-v1.5",

        "reranker":
        "cross-encoder/ms-marco-MiniLM-L-6-v2",

        "llm":
        "meta/llama-3.1-70b-instruct"

    }


@app.get("/stats")
def get_stats():

    documents = list(

        Path("documents").glob("*.pdf")

    )

    return {

        "status": "operational",

        "total_chunks":
        knowledge_engine.vector.collection.count(),

        "total_documents":
        len(documents),

        "graph":
        knowledge_engine.graph_statistics(),

        "documents":
        [

            doc.name

            for doc in documents

        ]

    }


@app.get("/documents")
def get_documents():

    return document_service.get_all_documents()


@app.get("/documents/search/{query}")
def search_documents(

    query: str

):

    return document_service.search(

        query

    )


@app.get("/documents/{filename}")
def get_document(

    filename: str

):

    document = document_service.get_document(

        filename

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    return document
@app.post("/upload")
async def upload_document(

    file: UploadFile = File(...)

):

    if not file.filename.endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are supported."

        )

    save_path = Path(

        "documents"

    ) / file.filename

    with open(

        save_path,

        "wb"

    ) as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    return {

        "status": "success",

        "filename": file.filename,

        "message": "PDF uploaded successfully.",

        "next_step": "Run ingest.py to index the document."

    }


@app.get("/equipment/{tag}")
def get_equipment_intelligence(

    tag: str

):

    try:

        return equipment_service.get_equipment_report(

            tag.upper()

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@app.get("/predict/{equipment_tag}")
def predict_equipment_health(

    equipment_tag: str

):

    try:

        result = knowledge_engine.equipment_search(

            equipment_tag.upper()

        )

        prediction = predictive_service.predict(

            result["documents"]

        )

        prediction["equipment_tag"] = equipment_tag.upper()

        prediction["confidence"] = result["confidence"]

        prediction["confidence_label"] = result["confidence_label"]

        return prediction

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@app.post("/ask")
def ask_question(

    request: QuestionRequest

):

    try:

        return chat_service.ask(

            question=request.question,

            equipment_tag=request.equipment_tag

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@app.get("/graph/statistics")
def graph_statistics():

    return knowledge_engine.graph_statistics()


@app.post("/graph/rebuild")
def rebuild_graph():

    return graph_service.rebuild()


@app.get("/graph/equipment/{tag}")
def equipment_graph(

    tag: str

):

    try:

        return graph_service.equipment_graph(

            tag.upper()

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@app.post("/graph/path")
def graph_path(

    request: GraphPathRequest

):

    try:

        path = graph_service.shortest_path(

            request.source,

            request.target

        )

        return {

            "source": request.source,

            "target": request.target,

            "path": path,

            "length": len(path)

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
@app.get("/reload")
def reload_knowledge():

    global knowledge_engine
    global predictive_service
    global graph_service
    global chat_service
    global equipment_service
    global document_service

    knowledge_engine = KnowledgeEngine()

    predictive_service = PredictiveService()

    graph_service = GraphService()

    chat_service = ChatService(

        knowledge_engine,

        llm

    )

    equipment_service = EquipmentService(

        knowledge_engine,

        llm

    )

    document_service = DocumentService()

    return {

        "status": "success",

        "message": "Knowledge engine, graph, and document service reloaded."

    }


@app.get("/version")
def version():

    return {

        "application": "MIRA",

        "version": "3.0.0",

        "backend": "FastAPI",

        "retrieval": "Hybrid Search (Vector + BM25 + Reranker)",

        "prediction": "Predictive Intelligence Engine",

        "embedding_model": "BAAI/bge-small-en-v1.5",

        "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2",

        "llm": "meta/llama-3.1-70b-instruct"

    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )
