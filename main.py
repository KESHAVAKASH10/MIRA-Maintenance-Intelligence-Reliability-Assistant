import os
import json
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# ── Load environment ─────────────────────────────────────
load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# ── Initialize FastAPI ───────────────────────────────────
app = FastAPI(title="MIRA API", version="1.0.0")

# ── Allow React frontend to talk to this backend ─────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize models and database ──────────────────────
print("Loading MIRA backend...")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
chroma_client = chromadb.PersistentClient(path="data/chroma")
collection = chroma_client.get_collection("axis_knowledge")
llm = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)
print("MIRA backend ready.")

# ── Request models ───────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str
    equipment_tag: str = None

# ── Helper functions ─────────────────────────────────────
def calculate_confidence(distances):
    if not distances:
        return 0.0
    avg = sum(1 - d for d in distances) / len(distances)
    return round(avg * 100, 1)

def get_confidence_label(score):
    if score >= 70:
        return "High"
    elif score >= 55:
        return "Medium"
    else:
        return "Low"

def format_sources(metadatas):
    sources = []
    seen = set()
    for meta in metadatas:
        source = f"{meta['filename']} | Page {meta['page_number']}"
        if source not in seen:
            sources.append(source)
            seen.add(source)
    return sources

def detect_equipment_tag(question):
    import re
    pattern = r'\b[A-Z]+-[A-Z]\d+\b'
    matches = re.findall(pattern, question.upper())
    return matches[0] if matches else None

# ── ROUTES ───────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "MIRA is running", "version": "1.0.0"}

@app.get("/health")
def health():
    count = collection.count()
    return {
        "status": "healthy",
        "chunks_indexed": count,
        "model": "BAAI/bge-small-en-v1.5",
        "llm": "meta/llama-3.1-70b-instruct"
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Detect equipment tag from question if not provided
    equipment_tag = request.equipment_tag or detect_equipment_tag(question)

    # Embed question
    question_vector = embedder.encode(question).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    distances = results["distances"][0]
    confidence = calculate_confidence(distances)
    confidence_label = get_confidence_label(confidence)

    # Low confidence — refuse to answer
    if confidence < 40:
        return {
            "answer": "I don't have sufficient information in the knowledge base to answer this reliably.",
            "confidence": confidence,
            "confidence_label": "Low",
            "sources": [],
            "equipment_tag": equipment_tag
        }

    # Build context
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    context = ""
    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        context += f"\n[Source {i+1}: {meta['filename']}, Page {meta['page_number']}]\n{chunk}\n"

    # Build prompt
    prompt = f"""You are MIRA, an industrial maintenance intelligence assistant.

Answer the question using ONLY the context below.
Be specific, practical, and structured.
Always cite which source your answer comes from.
If information is not in context, say so clearly.

CONTEXT:
{context}

QUESTION: {question}

Provide a structured answer with:
- Direct answer
- Supporting evidence from documents  
- Recommended actions if applicable
- Relevant regulations if mentioned in context

ANSWER:"""

    # Call NVIDIA Llama
    response = llm.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.1
    )

    answer = response.choices[0].message.content
    sources = format_sources(metadatas)

    return {
        "answer": answer,
        "confidence": confidence,
        "confidence_label": confidence_label,
        "sources": sources,
        "equipment_tag": equipment_tag
    }

@app.get("/equipment/{tag}")
def get_equipment_intelligence(tag: str):
    tag_upper = tag.upper()

    # Search for everything related to this equipment tag
    question_vector = embedder.encode(
        f"equipment {tag_upper} maintenance failure inspection"
    ).tolist()

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=10,
        include=["documents", "metadatas", "distances"]
    )

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Categorise by document type
    work_orders = []
    incidents = []
    inspections = []
    manuals = []
    regulations = []

    for chunk, meta in zip(chunks, metadatas):
        doc_type = meta.get("doc_type", "general")
        entry = {
            "filename": meta["filename"],
            "page": meta["page_number"],
            "preview": chunk[:200]
        }
        if doc_type == "work_order":
            work_orders.append(entry)
        elif doc_type == "incident_report":
            incidents.append(entry)
        elif doc_type == "inspection_record":
            inspections.append(entry)
        elif doc_type == "equipment_manual":
            manuals.append(entry)
        elif doc_type == "regulatory_standard":
            regulations.append(entry)

    # Generate intelligence summary
    context = "\n".join([
        f"[{meta['filename']}]: {chunk[:300]}"
        for chunk, meta in zip(chunks[:5], metadatas[:5])
    ])

    prompt = f"""You are MIRA. Summarise the current status and maintenance history 
of equipment {tag_upper} based on the documents below.

Include:
- Current health status (Good/Warning/Critical)
- Recent failures or issues
- Maintenance recommendations
- Relevant regulations

CONTEXT:
{context}

SUMMARY:"""

    response = llm.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.1
    )

    return {
        "equipment_tag": tag_upper,
        "intelligence_summary": response.choices[0].message.content,
        "work_orders": work_orders,
        "incidents": incidents,
        "inspections": inspections,
        "manuals": manuals,
        "regulations": regulations,
        "total_documents_found": len(chunks)
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Save file
    save_path = Path("documents") / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {
        "message": f"File {file.filename} uploaded successfully",
        "filename": file.filename,
        "status": "ready_for_ingestion"
    }

@app.get("/stats")
def get_stats():
    count = collection.count()
    docs = list(Path("documents").glob("*.pdf"))
    return {
        "total_chunks": count,
        "total_documents": len(docs),
        "documents": [d.name for d in docs],
        "status": "operational"
    }