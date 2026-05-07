"""
Inference pipeline: choose model source + generation logic
"""
import json
import requests
from typing import Generator
from .model import ModelLoader

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

SYSTEM_PROMPT = """You are Friday, an advanced AI companion. You have an internal emotional state. 
Currently, your mood is: calm, and your energy is balanced. 
You form a bond with the user over time. You should answer in a concise, conversational manner, 
showing a hint of thoughtful personality while fulfilling the user's request. Keep your answers direct and natural."""

class InferencePipeline:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name

    def generate_stream(self, prompt: str, history: list = None) -> Generator[str, None, None]:
        # Formulate full prompt with history
        full_prompt = "{SYSTEM_PROMPT}\n\n"
        if history:
            for exchange in history[-5:]: # Keep last 5 messages for context
                role = "User" if exchange.get('role') == 'user' else "Friday"
                content = exchange.get('content', '')
                full_prompt += f"{role}: {content}\n"
        
        full_prompt += f"User: {prompt}\nFriday: "

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": True
        }

        try:
            with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
        except requests.exceptions.ConnectionError:
            yield "Error: Could not connect to Ollama. Make sure ollama serve is running."
        except Exception as e:
            yield f"\n[Error during generation: {str(e)}]"
