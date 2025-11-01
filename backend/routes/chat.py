# backend/routes/chat.py
"""
Handles /chat endpoint — general chat using model pipeline
"""
from fastapi import APIRouter, HTTPException
from backend.core.model import ModelLoader
from backend.core.inference import InferencePipeline

router = APIRouter()

