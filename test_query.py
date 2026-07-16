import chromadb
from sentence_transformers import SentenceTransformer

# Load
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("axis_knowledge")

def search(question, n_results=4):
    # Embed the question
    question_vector = embedder.encode(question).tolist()
    
    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    print(f"\nQuestion: {question}")
    print("=" * 60)
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        relevance = round((1 - dist) * 100, 1)
        print(f"\nResult {i+1} — {relevance}% relevant")
        print(f"Source: {meta['filename']} | Page {meta['page_number']}")
        print(f"Type: {meta['doc_type']}")
        print(f"Text preview: {doc[:200]}...")

# Test with these 5 questions
search("What caused the failure on PUMP-P101?")
search("What is the LOTO procedure for rotating equipment?")
search("Which pumps need immediate attention?")
search("What does OISD-105 say about maintenance?")
search("What is the bearing replacement procedure?")