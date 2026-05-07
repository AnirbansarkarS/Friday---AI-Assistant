# frontend/helpers/api_client.py
"""
Handles API communication with FastAPI backend
"""
import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def listen(self):
        try:
            response = requests.get(f"{self.base_url}/listen")
            if response.status_code == 200:
                data = response.json()
                if "command" in data:
                    return data["command"]
            return None
        except Exception:
            return None

    def chat(self, message, history=None):
        if history is None:
            history = []
        payload = {"message": message, "history": history}
        try:
            response = requests.post(f"{self.base_url}/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Error getting response.")
        except Exception as e:
            return f"Error: {e}"

    def chat_stream(self, message, history=None):
        if history is None:
            history = []
            
        payload = {"message": message, "history": history}
        
        try:
            response = requests.post(f"{self.base_url}/chat", json=payload, stream=True)
            response.raise_for_status()
            
            # Yield characters or chunks as they arrive
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"\n[Network Error communicating with backend: {str(e)}]"

    def upload_doc(self, file):
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        response = requests.post(f"{self.base_url}/upload", files=files)
        return response.json()
