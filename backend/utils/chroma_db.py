"""
ChromaDB vector store interface for Friday AI
Uses the modern PersistentClient API (chromadb >= 0.4)
"""

import os
import hashlib
from typing import List, Optional
import chromadb

PERSIST_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "vectorstore"
)

# ---------------------------------------------------------------------------
# Client & collection (module-level singleton)
# ---------------------------------------------------------------------------

_client: Optional[chromadb.PersistentClient] = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        persist_path = os.path.abspath(PERSIST_DIR)
        os.makedirs(persist_path, exist_ok=True)
        _client = chromadb.PersistentClient(path=persist_path)
        _collection = _client.get_or_create_collection(
            name="friday_documents",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def _make_id(doc_name: str, chunk_index: int) -> str:
    """Deterministic ID so re-ingesting the same file is idempotent."""
    raw = f"{doc_name}::{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


def add_documents(
    chunks: List[str],
    embeddings: List[List[float]],
    doc_name: str,
) -> int:
    """
    Upsert text chunks with their embeddings into ChromaDB.

    Args:
        chunks     : list of text strings
        embeddings : list of float vectors (same length as chunks)
        doc_name   : source document name used for metadata + ID prefix

    Returns:
        Number of chunks upserted.
    """
    collection = _get_collection()
    ids = [_make_id(doc_name, i) for i in range(len(chunks))]
    metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


def similarity_search(
    query_embedding: List[float],
    n_results: int = 3,
) -> List[str]:
    """Return the top-n most similar text chunks."""
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        return []
    n = min(n_results, count)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
    )
    return results["documents"][0] if results["documents"] else []


def list_docs() -> List[str]:
    """Return unique document names currently stored in ChromaDB."""
    collection = _get_collection()
    if collection.count() == 0:
        return []
    all_data = collection.get(include=["metadatas"])
    seen = set()
    for meta in all_data.get("metadatas", []):
        if meta and "source" in meta:
            seen.add(meta["source"])
    return sorted(seen)


def delete_doc(doc_name: str) -> int:
    """Delete all chunks belonging to doc_name. Returns number deleted."""
    collection = _get_collection()
    all_data = collection.get(include=["metadatas"])
    ids_to_delete = [
        id_
        for id_, meta in zip(all_data["ids"], all_data["metadatas"])
        if meta and meta.get("source") == doc_name
    ]
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
    return len(ids_to_delete)


# ---------------------------------------------------------------------------
# ChromaDB class wrapper (backwards-compatible with old code)
# ---------------------------------------------------------------------------

class ChromaDB:
    def add_documents(self, chunks, embeddings, doc_name="unknown"):
        emb_list = embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings
        return add_documents(chunks, emb_list, doc_name)

    def similarity_search(self, query_embedding, n_results=3):
        qe = query_embedding.tolist() if hasattr(query_embedding, "tolist") else query_embedding
        return similarity_search(qe, n_results)

    def list_docs(self):
        return list_docs()

    def delete_doc(self, doc_name):
        return delete_doc(doc_name)


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.utils.chroma_db
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== ChromaDB Validation ===")

    sample_chunks = [
        "Friday is a personal AI assistant that knows me well.",
        "I enjoy hiking on weekends and playing guitar in the evening.",
        "My favourite programming language is Python.",
    ]
    # Fake embeddings (384-d zeros, matching MiniLM output dim)
    sample_embeddings = [[0.0] * 384 for _ in sample_chunks]

    print("\n1️⃣  Adding 3 sample chunks…")
    n = add_documents(sample_chunks, sample_embeddings, doc_name="test_doc")
    print(f"   ✅ Upserted {n} chunks.")

    print("\n2️⃣  Listing docs…")
    docs = list_docs()
    print(f"   Docs: {docs}")
    assert "test_doc" in docs, "Document not found after insertion!"

    print("\n3️⃣  Similarity search (zero vector)…")
    results = similarity_search([0.0] * 384, n_results=2)
    print(f"   Results: {results}")

    print("\n4️⃣  Deleting test_doc…")
    deleted = delete_doc("test_doc")
    print(f"   Deleted {deleted} chunks.")
    assert list_docs() == [] or "test_doc" not in list_docs()

    print("\n✅ ChromaDB test passed.")