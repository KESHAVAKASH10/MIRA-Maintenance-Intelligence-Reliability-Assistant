import os
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import json

# ── Load API key ─────────────────────────────────────────
load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# ── Initialize embedding model ───────────────────────────
print("Loading MIRA...")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

# ── Initialize ChromaDB ──────────────────────────────────
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("axis_knowledge")

# ── Initialize NVIDIA Llama ──────────────────────────────
llm = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# ── Calculate confidence score ───────────────────────────
def calculate_confidence(distances):
    if not distances:
        return 0.0
    avg_similarity = sum(1 - d for d in distances) / len(distances)
    return round(avg_similarity * 100, 1)

# ── Format sources for display ───────────────────────────
def format_sources(metadatas):
    sources = []
    seen = set()
    for meta in metadatas:
        source = f"{meta['filename']} | Page {meta['page_number']}"
        if source not in seen:
            sources.append(source)
            seen.add(source)
    return sources

# ── Main query function ──────────────────────────────────
def ask_mira(question, equipment_tag=None):
    # Step 1 — Convert question to vector
    question_vector = embedder.encode(question).tolist()

    # Step 2 — Search ChromaDB
    if equipment_tag:
        results = collection.query(
            query_embeddings=[question_vector],
            n_results=5,
            where={"equipment_tags": {"$ne": "[]"}},
            include=["documents", "metadatas", "distances"]
        )
    else:
        results = collection.query(
            query_embeddings=[question_vector],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )

    # Step 3 — Check confidence
    distances = results["distances"][0]
    confidence = calculate_confidence(distances)

    if confidence < 40:
        return {
            "answer": "I don't have sufficient information in the current knowledge base to answer this reliably. Please consult the relevant procedure document directly.",
            "sources": [],
            "confidence": confidence,
            "confidence_label": "Low"
        }

    # Step 4 — Build context from retrieved chunks
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""
    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        context += f"\n[Source {i+1}: {meta['filename']}, Page {meta['page_number']}]\n{chunk}\n"

    # Step 5 — Build prompt
    prompt = f"""You are MIRA, an industrial knowledge assistant for plant operations and maintenance.

Answer the question using ONLY the context provided below.
- Be specific and practical
- Always cite which source your answer comes from
- If the answer is not in the context, say "I don't have enough information on this topic"
- Keep the answer clear and actionable for a maintenance engineer

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 6 — Get answer from NVIDIA Llama
    response = llm.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.1
    )

    answer = response.choices[0].message.content

    # Step 7 — Format and return
    sources = format_sources(metadatas)
    confidence_label = "High" if confidence >= 70 else "Medium" if confidence >= 55 else "Low"

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "confidence_label": confidence_label
    }

# ── Interactive test ─────────────────────────────────────
if __name__ == "__main__":
    print("✅ MIRA is ready. Type your question or 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["quit", "exit", "q"]:
            print("Goodbye.")
            break

        if not question:
            continue

        print("\nMIRA is thinking...\n")
        result = ask_mira(question)

        print(f"MIRA: {result['answer']}")
        print(f"\nConfidence: {result['confidence_label']} ({result['confidence']}%)")
        print(f"Sources: {' | '.join(result['sources'])}")
        print("\n" + "="*60 + "\n")