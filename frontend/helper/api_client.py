import requests
import os


BASE = os.getenv("BACKEND_URL", "http://localhost:8000/api")




def chat(prompt: str):
    r = requests.post(f"{BASE}/chat", json={"prompt": prompt})
    return r.json()




def upload_pdf_file(path: str):
    with open(path, "rb") as f:
    r = requests.post(f"{BASE}/upload-pdf", files={"file": f})
    return r.json()




def ask_doc(question: str):
    r = requests.post(f"{BASE}/ask-doc", json={"question": question})
    return r.json()