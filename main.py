import os
import json
import shutil
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from services.utils.helpers import (
    calculate_confidence,
    get_confidence_label,
    format_sources,
    detect_equipment_tag,
)

# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

DOCUMENTS_FOLDER = "documents"
CHROMA_FOLDER = "data/chroma"
COLLECTION_NAME = "axis_knowledge"

# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI(
    title="MIRA API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# LOAD MODELS
# ==========================================================

print("\nLoading MIRA Backend...\n")

embedder = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = chroma_client.get_collection(
    COLLECTION_NAME
)

llm = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

print("✓ Embedding Model Loaded")
print("✓ Chroma Connected")
print("✓ NVIDIA Llama Connected")
print("✓ MIRA Backend Ready\n")

# ==========================================================
# REQUEST MODELS
# ==========================================================

class QuestionRequest(BaseModel):
    question: str
    equipment_tag: str | None = None

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def build_context(documents, metadatas):

    context = []

    for document, metadata in zip(documents, metadatas):

        context.append(
            f"""
SOURCE:
File : {metadata['filename']}
Page : {metadata['page_number']}
Type : {metadata.get('doc_type','general')}

CONTENT:
{document}
"""
        )

    return "\n\n".join(context)


def classify_documents(documents, metadatas):

    work_orders = []
    incidents = []
    inspections = []
    manuals = []
    regulations = []

    for doc, meta in zip(documents, metadatas):

        item = {
            "filename": meta["filename"],
            "page": meta["page_number"],
            "preview": doc[:200]
        }

        doc_type = meta.get("doc_type", "general_document")

        if doc_type == "work_order":
            work_orders.append(item)

        elif doc_type == "incident_report":
            incidents.append(item)

        elif doc_type == "inspection_record":
            inspections.append(item)

        elif doc_type == "equipment_manual":
            manuals.append(item)

        elif doc_type == "regulatory_standard":
            regulations.append(item)

    return (
        work_orders,
        incidents,
        inspections,
        manuals,
        regulations,
    )

# ==========================================================
# BASIC ROUTES
# ==========================================================

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
        "chunks_indexed": collection.count(),
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "llm": "meta/llama-3.1-70b-instruct"
    }

# ==========================================================
# ASK ENDPOINT
# ==========================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if question == "":
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    equipment_tag = request.equipment_tag

    if equipment_tag is None:
        equipment_tag = detect_equipment_tag(question)

    question_embedding = embedder.encode(question).tolist()

    query_args = {
        "query_embeddings": [question_embedding],
        "n_results": 5,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if equipment_tag:
        query_args["where"] = {
            "equipment_tag": equipment_tag.upper()
        }

    results = collection.query(**query_args)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if len(documents) == 0:

        return {
            "answer": "No relevant information was found in the knowledge base.",
            "confidence": 0,
            "confidence_label": "Low",
            "equipment_tag": equipment_tag,
            "sources": []
        }

    confidence = calculate_confidence(distances)
    confidence_label = get_confidence_label(confidence)

    if confidence < 40:

        return {
            "answer": "I don't have enough reliable information to answer this question confidently.",
            "confidence": confidence,
            "confidence_label": confidence_label,
            "equipment_tag": equipment_tag,
            "sources": []
        }

    context = build_context(documents, metadatas)

    prompt = f"""
You are MIRA (Maintenance Intelligence & Reliability Assistant).

Answer ONLY from the provided context.

Rules:

- Never invent information.
- If something is not available, clearly say it.
- Mention filenames whenever useful.
- Give practical maintenance recommendations.
- Mention regulations if present.

==========================
CONTEXT
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""

    response = llm.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=650
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "confidence": confidence,
        "confidence_label": confidence_label,
        "equipment_tag": equipment_tag,
        "sources": format_sources(metadatas)
    }

# ==========================================================
# EQUIPMENT 360
# ==========================================================

@app.get("/equipment/{tag}")
def get_equipment_intelligence(tag: str):

    tag = tag.upper()

    question_embedding = embedder.encode(
        f"{tag} maintenance history failures inspection work order incidents"
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        where={"equipment_tag": tag},
        n_results=15,
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if len(documents) == 0:

        return {
            "equipment_tag": tag,
            "status": "not_found",
            "message": f"No information found for {tag}.",
            "intelligence_summary": "",
            "health_status": "Unknown",
            "confidence": 0,
            "work_orders": [],
            "incidents": [],
            "inspections": [],
            "manuals": [],
            "regulations": [],
            "sources": [],
            "total_documents_found": 0
        }

    confidence = calculate_confidence(distances)

    (
        work_orders,
        incidents,
        inspections,
        manuals,
        regulations
    ) = classify_documents(documents, metadatas)

    context = build_context(documents, metadatas)

    prompt = f"""
You are MIRA.

Generate an Equipment 360 report.

Equipment Tag : {tag}

Only use the supplied context.

Return exactly in this structure.

## Health Status
Healthy / Warning / Critical

## Executive Summary

## Recent Issues

## Maintenance Recommendations

## Relevant Regulations

Do not invent information.

CONTEXT

{context}
"""

    response = llm.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=700
    )

    summary = response.choices[0].message.content
    summary_lower = summary.lower()

    if "critical" in summary_lower:
        health = "Critical"
    elif "warning" in summary_lower:
        health = "Warning"
    else:
        health = "Healthy"

    return {
        "equipment_tag": tag,
        "health_status": health,
        "confidence": confidence,
        "confidence_label": get_confidence_label(confidence),
        "intelligence_summary": summary,
        "work_orders": work_orders,
        "incidents": incidents,
        "inspections": inspections,
        "manuals": manuals,
        "regulations": regulations,
        "sources": format_sources(metadatas),
        "total_documents_found": len(documents)
    }

# ==========================================================
# UPLOAD DOCUMENT
# ==========================================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    documents_path = Path(DOCUMENTS_FOLDER)
    documents_path.mkdir(parents=True, exist_ok=True)
    save_path = documents_path / file.filename

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {
        "status": "success",
        "filename": file.filename,
        "location": str(save_path),
        "message": "Document uploaded successfully. Run ingest.py to index it."
    }

# ==========================================================
# STATS
# ==========================================================

@app.get("/stats")
def get_stats():

    docs = list(Path(DOCUMENTS_FOLDER).glob("*.pdf"))

    return {
        "backend": "healthy",
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "llm": "meta/llama-3.1-70b-instruct",
        "total_documents": len(docs),
        "total_chunks": collection.count(),
        "documents": [d.name for d in docs]
    }