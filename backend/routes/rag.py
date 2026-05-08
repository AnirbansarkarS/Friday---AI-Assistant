# backend/routes/rag.py
"""
RAG API routes:
  POST /rag/upload       — ingest a PDF or TXT file
  GET  /rag/docs         — list indexed documents
  DELETE /rag/docs/{name} — remove a document from the store
"""

import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.utils.ingest import ingest_file
from backend.utils.chroma_db import list_docs, delete_doc

router = APIRouter(prefix="/rag")

DOCS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "docs")
)
os.makedirs(DOCS_DIR, exist_ok=True)


@router.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    """
    Accept a PDF or TXT upload, save it to data/docs/, and ingest it into ChromaDB.
    Returns: {"doc_name": str, "chunks": int}
    """
    allowed_exts = {".pdf", ".txt", ".md"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: PDF, TXT, MD",
        )

    save_path = os.path.join(DOCS_DIR, file.filename)
    try:
        with open(save_path, "wb") as out:
            shutil.copyfileobj(file.file, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    try:
        result = ingest_file(save_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return result


@router.get("/docs")
async def get_docs():
    """Return list of document names currently indexed in ChromaDB."""
    try:
        docs = list_docs()
        return {"docs": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/docs/{doc_name:path}")
async def remove_doc(doc_name: str):
    """Delete all ChromaDB chunks for the given document name."""
    try:
        deleted = delete_doc(doc_name)
        return {"doc_name": doc_name, "chunks_deleted": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
