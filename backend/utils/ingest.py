"""
File ingestor for Friday AI RAG pipeline.
Supports PDF and plain-text files.
Pipeline: load → split → embed → store in ChromaDB
"""

import os
from typing import Optional

from backend.utils.pdf_loader import load_pdf, load_txt
from backend.utils.text_splitter import split_text
from backend.core.embedding import Embeddings
from backend.utils.chroma_db import add_documents

# Singleton embedder (lazy-loaded)
_embedder: Optional[Embeddings] = None


def _get_embedder() -> Embeddings:
    global _embedder
    if _embedder is None:
        _embedder = Embeddings()
    return _embedder


def ingest_file(filepath: str) -> dict:
    """
    Ingest a PDF or TXT file into ChromaDB.

    Args:
        filepath: absolute path to the file

    Returns:
        {"doc_name": str, "chunks": int}
    """
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    doc_name = os.path.basename(filepath)

    print(f"📄 Loading: {doc_name}")
    if ext == ".pdf":
        raw_text = load_pdf(filepath)
    elif ext in (".txt", ".md"):
        raw_text = load_txt(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use PDF or TXT.")

    if not raw_text or not raw_text.strip():
        raise ValueError(f"No text extracted from {doc_name}.")

    print(f"✂️  Splitting into chunks…")
    chunks = split_text(raw_text, chunk_size=500, overlap=50)
    print(f"   {len(chunks)} chunks created.")

    print(f"🧬 Embedding chunks…")
    embedder = _get_embedder()
    embeddings = embedder.encode(chunks)

    print(f"💾 Storing in ChromaDB…")
    emb_list = embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings
    stored = add_documents(chunks, emb_list, doc_name=doc_name)
    print(f"✅ Ingested {stored} chunks for '{doc_name}'.")

    return {"doc_name": doc_name, "chunks": stored}


# ---------------------------------------------------------------------------
# Standalone test — run: python -m backend.utils.ingest
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m backend.utils.ingest <path/to/file.pdf or .txt>")
        sys.exit(1)
    result = ingest_file(sys.argv[1])
    print(f"\n🎉 Done! {result}")
