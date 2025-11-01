# backend/routes/health.py
"""
Simple health check endpoint
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "message": "Server running smoothly 🚀"}