"""
Loads AI models: Ollama (local) + Hugging Face fallback
"""
from huggingface_hub import InferenceClient
import subprocess
import requests

class ModelLoader:
    def __init__(self, ollama_model="llama3", hf_model="gpt2", hf_api_key=None):
        self.ollama_model = ollama_model
        self.hf_client = InferenceClient(hf_model, token=hf_api_key) if hf_api_key else None

    def generate_ollama(self, prompt):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.ollama_model, "prompt": prompt}, timeout=30
            )
            return response.json().get("response", "")
        except:
            return None

    def generate_hf(self, prompt):
        if not self.hf_client:
            return "HF API Key missing"
        return self.hf_client.text_generation(prompt)