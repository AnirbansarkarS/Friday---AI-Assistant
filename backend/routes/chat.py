# backend/routes/chat.py
"""
Handles /chat endpoint - general chat using model pipeline
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.core.inference import InferencePipeline

router = APIRouter()
pipeline = InferencePipeline()

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = []

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return StreamingResponse(
        pipeline.generate_stream(req.message, req.history),
        media_type="text/event-stream"
    )
