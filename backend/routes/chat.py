# backend/routes/chat.py
"""
/chat endpoint — RAG-augmented streaming chat
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.core.inference import InferencePipeline
from backend.core.embedding import Embeddings
from backend.utils.chroma_db import similarity_search

router = APIRouter()
pipeline = InferencePipeline()

# Lazy singleton embedder
_embedder: Optional[Embeddings] = None

def _get_embedder() -> Embeddings:
    global _embedder
    if _embedder is None:
        _embedder = Embeddings()
    return _embedder


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = []


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # RAG: embed the user query and retrieve relevant chunks
    rag_context = ""
    try:
        embedder = _get_embedder()
        query_vec = embedder.encode([req.message])[0].tolist()
        chunks = similarity_search(query_vec, n_results=3)
        if chunks:
            rag_context = "\n---\n".join(chunks)
    except Exception:
        pass  # RAG failure is non-fatal — fall through to plain LLM

    return StreamingResponse(
        pipeline.generate_stream(req.message, req.history, rag_context=rag_context),
        media_type="text/event-stream",
    )
