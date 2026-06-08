import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

folder = Path("housing_docs")
folder.mkdir(exist_ok=True)




# Configuration
CHUNK_SIZE = 100
OVERLAP = 40

def clean_text(text):
    """
    Basic text cleaning:
    - Remove extra whitespace
    - Remove URLs
    - Remove special characters (optional)
    """
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)

    # Remove extra symbols while keeping punctuation
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)

    return text.strip()


def chunk_text(text, chunk_size=100, overlap=40):
    """
    Create overlapping chunks.
    """
    
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += (chunk_size - overlap)

    return chunks


def load_documents(folder_path):
    """
    Load all .txt files from a directory.
    """
    
    documents = []

    for file in Path(folder_path).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            documents.append({
                "source": file.name,
                "text": f.read()
            })

    return documents


# Example usage
documents = load_documents("housing_docs")

all_chunks = []
chunk_counter=0

for doc in documents:
    cleaned_text = clean_text(doc["text"])

    chunks = chunk_text(
        cleaned_text,
        chunk_size=CHUNK_SIZE,
        overlap=OVERLAP
    )

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "source": doc["source"],
            "chunk_id": i,
            "text": chunk
        })
    chunk_counter+=1
print("Total chunks :", chunk_counter)
texts = [c["text"] for c in all_chunks]

embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=True
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="housing_docs",
    metadata={"hnsw:space": "cosine"}  # required for BGE embeddings
)

for i, chunk in enumerate(all_chunks):
    collection.add(
        ids=[f"{chunk['source']}::{chunk['chunk_id']}"],
        embeddings=[embeddings[i].tolist()],
        documents=[chunk["text"]],
        metadatas=[{
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }]
    )

print("Indexing complete.")
def retrieve(query: str, k: int = 5):
    """
    Retrieve top-k relevant chunks for a query.
    Returns chunk text, source metadata, and similarity scores.
    """
    query_embedding = model.encode(
        QUERY_PREFIX + query,       # BGE requires prefix on queries only
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []
    for text, meta, dist in zip(documents, metadatas, distances):
        retrieved.append({
            "text":     text,
            "source":   meta.get("source",   "unknown"),
            "chunk_id": meta.get("chunk_id", "unknown"),
            "score":    round(1.0 - dist, 4),  # cosine distance → similarity
        })

    return retrieved
if collection.count() == 0:
    for i, chunk in enumerate(all_chunks):
        collection.add(
            ids=[f"{chunk['source']}::{chunk['chunk_id']}"],
            embeddings=[embeddings[i].tolist()],
            documents=[chunk["text"]],
            metadatas=[{
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            }]
        )
    print("Indexing complete.")
else:
    print(f"Collection already has {collection.count()} chunks, skipping indexing.")
    hits = retrieve("Price of off campus living?", k=5)
for i, hit in enumerate(hits, 1):
    print(f"\n[{i}] Score : {hit['score']}")
    print(f"    Source: {hit['source']}  (chunk {hit['chunk_id']})")
    print(f"    Text  : {hit['text']}")