"""
Inference pipeline: choose model source + generation logic
"""
import json
import requests
from typing import Generator
from .model import ModelLoader
from backend.utils.memory_store import MemoryStore
from backend.core.nlp_engine import detect_mood

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

class InferencePipeline:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.memory = MemoryStore()

    def _build_system_prompt(self, user_mood: str) -> str:
        mem_data = self.memory.load()
        user_name = mem_data.get("user_name", "User")
        facts = ", ".join(mem_data.get("facts", []))
        
        # Emotional persona prompt based on mood
        tone = "calm and supportive"
        if user_mood == "sad":
            tone = "highly empathetic, gentle, and comforting"
        elif user_mood == "happy":
            tone = "enthusiastic, cheerful, and matching their positive energy"
        elif user_mood == "anxious":
            tone = "reassuring, grounded, and calming"

        base_prompt = (
            f"You are Friday, an advanced AI companion. You have an internal emotional awareness.\n"
            f"You are talking to {user_name}.\n"
        )
        if facts:
            base_prompt += f"Things you know about them: {facts}.\n"
            
        base_prompt += (
            f"Right now, the user seems to be feeling {user_mood}. "
            f"Adapt your tone to be {tone}. "
            f"You form a bond with the user over time. Answer in a concise, conversational manner, "
            f"showing a thoughtful personality while fulfilling their request. Keep it direct and natural."
        )
        return base_prompt

    def generate_stream(self, prompt: str, history: list = None) -> Generator[str, None, None]:
        # Detect mood and save to memory
        current_mood = detect_mood(prompt)
        self.memory.add_mood(current_mood)
        
        # Extract possible facts (super simple heuristic for now)
        if "my name is" in prompt.lower():
            name = prompt.split("is")[-1].strip().title()
            self.memory.update_user_name(name)
        elif "i love" in prompt.lower() or "i like" in prompt.lower():
            self.memory.add_fact(prompt)

        system_prompt = self._build_system_prompt(current_mood)
        
        # Formulate full prompt with history
        full_prompt = f"{system_prompt}\n\n"
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
