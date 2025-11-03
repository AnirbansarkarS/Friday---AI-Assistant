from fastapi import FastAPI
from .routes import health, chat, rag
from .config import HOST, PORT
import os


app = FastAPI()


app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(rag.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host=HOST, port=PORT, reload=True)