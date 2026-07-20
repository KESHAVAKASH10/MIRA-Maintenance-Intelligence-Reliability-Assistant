import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pathlib import Path
import shutil

from dotenv import load_dotenv
from openai import OpenAI

from services.knowledge_engine import KnowledgeEngine
from services.chat_service import ChatService
from services.equipment_service import EquipmentService

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

chat_service = ChatService(
    knowledge_engine,
    llm
)

equipment_service = EquipmentService(
    knowledge_engine,
    llm
)

print("MIRA Backend Ready.")


class QuestionRequest(BaseModel):
    question: str
    equipment_tag: str | None = None


@app.get("/")
def root():

    return {
        "status": "MIRA is running",
        "version": "2.0.0"
    }


@app.get("/health")
def health():

    return {

        "status": "healthy",

        "chunks_indexed":
        knowledge_engine.vector.collection.count(),

        "embedding_model":
        "BAAI/bge-small-en-v1.5",

        "reranker":
        "cross-encoder/ms-marco-MiniLM-L-6-v2",

        "llm":
        "meta/llama-3.1-70b-instruct"

    }@app.get("/stats")
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

        "documents":
        [

            doc.name

            for doc in documents

        ]

    }


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


@app.get("/reload")
def reload_knowledge():

    global knowledge_engine
    global chat_service
    global equipment_service

    knowledge_engine = KnowledgeEngine()

    chat_service = ChatService(

        knowledge_engine,

        llm

    )

    equipment_service = EquipmentService(

        knowledge_engine,

        llm

    )

    return {

        "status": "success",

        "message": "Knowledge engine reloaded."

    }


@app.get("/version")
def version():

    return {

        "application": "MIRA",

        "version": "2.0.0",

        "backend": "FastAPI",

        "retrieval": "Hybrid Search (Vector + BM25 + Reranker)",

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