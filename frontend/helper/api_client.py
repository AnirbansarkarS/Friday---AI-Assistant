# frontend/helpers/api_client.py
"""
Handles API communication with FastAPI backend
"""
import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def chat(self, message):
        response = requests.post(f"{self.base_url}/chat", json={"message": message})
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return f"Error: {response.text}"

    def upload_doc(self, file):
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        response = requests.post(f"{self.base_url}/upload", files=files)
        if response.status_code == 200:
            return response.json().get("message")
        else:
            return f"Error: {response.text}"

    def ask_doc(self, question):
        response = requests.post(f"{self.base_url}/ask-doc", json={"question": question})
        if response.status_code == 200:
            return response.json().get("answer")
        else:
            return f"Error: {response.text}"