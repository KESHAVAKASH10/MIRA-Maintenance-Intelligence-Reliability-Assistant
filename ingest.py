import os
import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import re

# ── Config ──────────────────────────────────────────────
DOCS_FOLDER = "documents"
CHROMA_FOLDER = "data/chroma"
CHUNK_SIZE = 400        # words per chunk
CHUNK_OVERLAP = 50      # words overlap between chunks

# ── Equipment tags to watch for ─────────────────────────
EQUIPMENT_TAGS = [
    "PUMP-P101", "PUMP-P102", "PUMP-P103",
    "COMP-C201", "VALVE-V301"
]

# ── Regulation references to watch for ──────────────────
REGULATION_REFS = [
    "OISD-105", "OISD-118", "OISD-137",
    "Factories Act", "Section 36", "Section 92",
    "DGMS", "PESO"
]

# ── Initialize embedding model (free, runs locally) ─────
print("Loading embedding model...")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
print("Embedding model loaded.")

# ── Initialize ChromaDB ─────────────────────────────────
client = chromadb.PersistentClient(path=CHROMA_FOLDER)
collection = client.get_or_create_collection(
    name="axis_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# ── Helper: Extract text from PDF ───────────────────────
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # skip blank pages
            pages.append({
                "text": text,
                "page_number": page_num + 1
            })
    doc.close()
    return pages

# ── Helper: Split text into overlapping chunks ───────────
def chunk_text(text, page_number, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        
        chunks.append({
            "text": chunk_text,
            "page_number": page_number,
            "chunk_index": chunk_index
        })
        
        chunk_index += 1
        start += chunk_size - overlap
    
    return chunks

# ── Helper: Detect equipment tags in text ───────────────
def detect_equipment_tags(text):
    found = []
    for tag in EQUIPMENT_TAGS:
        if tag in text:
            found.append(tag)
    # Also detect generic patterns like PUMP-P104
    pattern = r'\b[A-Z]+-[A-Z]\d+\b'
    generic = re.findall(pattern, text)
    found.extend(generic)
    return list(set(found))

# ── Helper: Detect regulation references in text ────────
def detect_regulation_refs(text):
    found = []
    for ref in REGULATION_REFS:
        if ref in text:
            found.append(ref)
    return found

# ── Helper: Detect document type from filename ──────────
def detect_doc_type(filename):
    filename_lower = filename.lower()
    if "work_order" in filename_lower or "wo_" in filename_lower:
        return "work_order"
    elif "incident" in filename_lower or "inc_" in filename_lower:
        return "incident_report"
    elif "inspection" in filename_lower or "checklist" in filename_lower:
        return "inspection_record"
    elif "sop" in filename_lower or "procedure" in filename_lower or "loto" in filename_lower:
        return "safety_procedure"
    elif "oisd" in filename_lower:
        return "regulatory_standard"
    elif "factories_act" in filename_lower:
        return "regulatory_standard"
    elif "manual" in filename_lower:
        return "equipment_manual"
    else:
        return "general_document"

# ── Main ingestion function ──────────────────────────────
def ingest_document(pdf_path):
    filename = Path(pdf_path).name
    doc_type = detect_doc_type(filename)
    
    print(f"\nIngesting: {filename}")
    print(f"  Document type: {doc_type}")
    
    # Extract text page by page
    pages = extract_text_from_pdf(pdf_path)
    print(f"  Pages extracted: {len(pages)}")
    
    all_chunks = []
    
    # Chunk each page
    for page in pages:
        chunks = chunk_text(page["text"], page["page_number"])
        all_chunks.extend(chunks)
    
    print(f"  Total chunks: {len(all_chunks)}")
    
    # Process each chunk
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(all_chunks):
        # Detect entities in this chunk
        equipment_tags = detect_equipment_tags(chunk["text"])
        regulation_refs = detect_regulation_refs(chunk["text"])
        
        # Create unique ID
        chunk_id = f"{filename}__page{chunk['page_number']}__chunk{i}"
        
        # Generate embedding
        embedding = embedder.encode(chunk["text"]).tolist()
        
        # Build metadata
        metadata = {
            "filename": filename,
            "doc_type": doc_type,
            "page_number": chunk["page_number"],
            "chunk_index": i,
            "equipment_tags": json.dumps(equipment_tags),
            "regulation_refs": json.dumps(regulation_refs),
            "has_equipment_tag": len(equipment_tags) > 0,
            "has_regulation_ref": len(regulation_refs) > 0,
        }
        
        ids.append(chunk_id)
        embeddings.append(embedding)
        documents.append(chunk["text"])
        metadatas.append(metadata)
    
    # Store in ChromaDB in batches of 100
    batch_size = 100
    for start in range(0, len(ids), batch_size):
        end = min(start + batch_size, len(ids))
        collection.upsert(
            ids=ids[start:end],
            embeddings=embeddings[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end]
        )
    
    print(f"  ✅ Stored {len(all_chunks)} chunks in ChromaDB")
    return len(all_chunks)

# ── Run ingestion for all PDFs ───────────────────────────
def ingest_all():
    docs_path = Path(DOCS_FOLDER)
    pdf_files = list(docs_path.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in documents/ folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print("=" * 50)
    
    total_chunks = 0
    for pdf_file in pdf_files:
        chunks = ingest_document(str(pdf_file))
        total_chunks += chunks
    
    print("\n" + "=" * 50)
    print(f"✅ INGESTION COMPLETE")
    print(f"   Documents processed: {len(pdf_files)}")
    print(f"   Total chunks stored: {total_chunks}")
    print(f"   ChromaDB location: {CHROMA_FOLDER}")

if __name__ == "__main__":
    ingest_all()