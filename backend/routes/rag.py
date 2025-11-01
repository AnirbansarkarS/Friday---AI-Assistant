# Initialize model loader and pipeline once
loader = ModelLoader()
pipe = InferencePipeline(loader)

@router.post("/chat")
def chat(request: dict):
    try:
        user_input = request.get("message", "")
        if not user_input:
            raise HTTPException(status_code=400, detail="Message required")
        response = pipe.generate(user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# backend/routes/rag.py
"""
Handles /ask-doc endpoint — RAG system for document-based QA
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.pdf_loader import load_pdf
from backend.utils.text_splitter import split_text
from backend.utils.chroma_db import ChromaDB
from backend.core.embeddings import Embeddings
from backend.core.rag import RAG
from backend.core.inference import InferencePipeline
from backend.core.model import ModelLoader

router = APIRouter()

vector_store = ChromaDB()
embedder = Embeddings()
loader = ModelLoader()
pipe = InferencePipeline(loader)
rag = RAG(pipe, vector_store)

@router.post("/upload")
def upload_doc(file: UploadFile = File(...)):
    try:
        text = load_pdf(file.file)
        chunks = split_text(text)
        embeddings = embedder.encode(chunks)
        vector_store.add_documents(chunks, embeddings)
        return {"message": "Document uploaded and indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask-doc")
def ask_doc(request: dict):
    try:
        query = request.get("question", "")
        if not query:
            raise HTTPException(status_code=400, detail="Question required")
        answer = rag.query(query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



