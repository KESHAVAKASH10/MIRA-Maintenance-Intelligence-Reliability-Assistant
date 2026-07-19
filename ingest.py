import re
import json
import fitz
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

DOCS_FOLDER = "documents"
CHROMA_FOLDER = "data/chroma"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

print("Loading embedding model...")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
print("Embedding model loaded.")

client = chromadb.PersistentClient(path=CHROMA_FOLDER)

try:
    client.delete_collection("axis_knowledge")
except:
    pass

collection = client.create_collection(
    name="axis_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def extract_text(pdf):
    doc = fitz.open(pdf)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()

        if text.strip():
            pages.append(
                {
                    "page": i + 1,
                    "text": text
                }
            )

    doc.close()
    return pages


def chunk_text(text, page):
    words = text.split()

    chunks = []

    start = 0
    idx = 0

    while start < len(words):

        end = min(start + CHUNK_SIZE, len(words))

        chunks.append(
            {
                "page": page,
                "chunk": idx,
                "text": " ".join(words[start:end])
            }
        )

        idx += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def detect_doc_type(filename):

    f = filename.lower()

    if "wo_" in f or "work_order" in f:
        return "work_order"

    if "incident" in f or "inc_" in f:
        return "incident_report"

    if "inspection" in f or "checklist" in f:
        return "inspection_record"

    if "manual" in f:
        return "equipment_manual"

    if "oisd" in f or "factories" in f:
        return "regulatory_standard"

    return "general_document"


def ingest(pdf):

    filename = Path(pdf).name

    print(f"\nProcessing {filename}")

    pages = extract_text(pdf)

    doc_type = detect_doc_type(filename)

    ids = []
    docs = []
    embeds = []
    metas = []

    for page in pages:

        chunks = chunk_text(page["text"], page["page"])

        for chunk in chunks:

            text = chunk["text"]

            embedding = embedder.encode(text).tolist()

            equipment_tags = list(
                set(
                    re.findall(
                        r"[A-Z]+-[A-Z]\d+",
                        text
                    )
                )
            )

            regulation_refs = list(
                set(
                    re.findall(
                        r"OISD-\d+|Factories Act|DGMS|PESO",
                        text
                    )
                )
            )

            if len(equipment_tags) == 0:
                equipment_tags = ["GENERAL"]

            for tag in equipment_tags:

                ids.append(
                    f"{filename}_{chunk['page']}_{chunk['chunk']}_{tag}"
                )

                docs.append(text)

                embeds.append(embedding)

                metas.append(
                    {
                        "filename": filename,
                        "page_number": chunk["page"],
                        "chunk_index": chunk["chunk"],
                        "doc_type": doc_type,
                        "equipment_tag": tag,
                        "equipment_tags": json.dumps(equipment_tags),
                        "regulation_refs": json.dumps(regulation_refs),
                        "has_equipment_tag": tag != "GENERAL",
                        "has_regulation_ref": len(regulation_refs) > 0
                    }
                )

    collection.upsert(
        ids=ids,
        embeddings=embeds,
        documents=docs,
        metadatas=metas
    )

    print(f"Stored {len(ids)} vectors")


def ingest_all():

    pdfs = list(Path(DOCS_FOLDER).glob("*.pdf"))

    print(f"\nFound {len(pdfs)} PDFs\n")

    for pdf in pdfs:
        ingest(str(pdf))

    print("\nDone.")
    print("Total vectors:", collection.count())


if __name__ == "__main__":
    ingest_all()