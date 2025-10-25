import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "gpt2") # conservative default (replace with chat-capable model)
CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/vectorstore")

# FastAPI host/port
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))